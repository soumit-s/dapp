# Entry point for the outbox worker app
import asyncio
import uuid
import signal
import logging
import os

from .db import async_session_factory
from .workers.outbox_worker import OutboxWorker
from .workers.outbox_worker import OutboxWorker, OutboxKafkaConfig
from .config import config


async def main():
    if os.getenv("MODE", "production") == "development":
        logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_running_loop()
    outbox_worker_stop_signal = asyncio.Event()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, outbox_worker_stop_signal.set)

    outbox_kafka_config = OutboxKafkaConfig(
        brokers=config.kafka_brokers,
        client_id=config.kafka_client_id,
        topic=config.kafka_user_topic,
    )
    await OutboxWorker(
        worker_id=str(uuid.uuid4()),
        session_factory=async_session_factory,
        config=outbox_kafka_config,
    ).run(outbox_worker_stop_signal)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
