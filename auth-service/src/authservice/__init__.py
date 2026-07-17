from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from .db import async_engine, async_session_factory
from .schema import Base
from .router import router
from .config import config
from .services import UserService, PasswordService
from .errors import EmailAlreadyTakenError, RoleAlreadyExistsError


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("MODE", "production") == "development":
        # Push schema
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
    
        async with async_session_factory() as session:
            password_service = PasswordService()
            user_service = UserService(session=session, config=config)
            # Create the admin role
            try:
                await user_service.create_role(config.role_name_user)
            except RoleAlreadyExistsError:
                pass
            # Create the user role.
            try:
                await user_service.create_role(config.role_name_admin)
            except RoleAlreadyExistsError:
                pass  
            # Create admin user
            try:
                await user_service.create_admin("admin@dapp.com", password_service.hash_pwd("admin"))
                print("Successfully created admin user")
            except EmailAlreadyTakenError:
                pass

    # outbox_worker_stop_signal = asyncio.Event()
    # outbox_kafka_config = OutboxKafkaConfig(
    #     brokers=config.kafka_brokers,
    #     client_id=config.kafka_client_id,
    #     topic=config.kafka_user_topic,
    # )
    # outbox_worker_task = asyncio.create_task(
    #     OutboxWorker(
    #         worker_id=str(uuid.uuid4()),
    #         session_factory=async_session_factory,
    #         config=outbox_kafka_config,
    #     ).run(outbox_worker_stop_signal)
    # )

    yield

    # # Stop the worker.
    # outbox_worker_stop_signal.set()
    # await outbox_worker_task


app = FastAPI(lifespan=lifespan)
# print(f"Allowed Origins: {config.allowed_origins}")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=config.allowed_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(router)
