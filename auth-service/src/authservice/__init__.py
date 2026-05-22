from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import asyncio
import uuid

from .db import async_engine, async_session_factory
from .schema import Base
from .router import router
from .workers.outbox_worker import OutboxWorker, OutboxKafkaConfig
from .config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("MODE", "production") == "development":
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
