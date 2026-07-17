from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from .router import router
from .schema import Base
from .deps import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # If it is in a development environment, push the schema
    # to the database.
    if os.getenv("MODE") == "development":
        print("Pushing database schema")
        db = get_db()
        async with db.get_async_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Start the Outbox Worker
    # outbox_worker_stop_signal = asyncio.Event()
    # outbox_worker_task = asyncio.create_task(
    #     OutboxWorker(
    #         stop_signal=outbox_worker_stop_signal, session_factory=async_session_factory
    #     ).run()
    # )

    yield

    print("Shutting down application")

    # Gracefully stop the outbox worker
    # print("Telling outbox worker to stop")
    # outbox_worker_stop_signal.set()
    # await outbox_worker_task
    # print("Outbox Worker stopped gracefully")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)
app.include_router(router)
