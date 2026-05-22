from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession
from sqlalchemy import func, select, delete, update, literal
from sqlalchemy.dialects.postgresql import insert as pg_insert
from dataclasses import dataclass
from confluent_kafka.aio import AIOProducer
import asyncio
import json
from datetime import timedelta
import logging

from ..schema import AggregateLock, OutboxEvent
from ..models import OutboxEventDTO


@dataclass
class OutboxKafkaConfig:
    brokers: str
    client_id: str
    topic: str


class OutboxWorker:
    def __init__(
        self,
        worker_id: str,
        session_factory: async_sessionmaker[AsyncSession],
        config: OutboxKafkaConfig,
    ):
        self.worker_id = worker_id
        self.session_factory = session_factory
        self.config = config

    async def run(self, stop_signal: asyncio.Event):
        self.producer = AIOProducer(
            {
                "bootstrap.servers": self.config.brokers,
                "client.id": f"{self.config.client_id}:{self.worker_id}",
            }
        )
        try:
            while not stop_signal.is_set():
                # Check for locks that have expired (5s) and delete them.
                deleted_locks = await self.delete_expired_locks()
                if deleted_locks:
                    logging.info("Deleted the following expired locks: ")
                    logging.info(deleted_locks)
                # Lock aggregates
                aggregates = await self.lock_aggregates()
                if aggregates:
                    logging.info("Locked aggregates: ")
                    logging.info(aggregates)
                # Process each aggregate
                for aggregate_id in aggregates:
                    events = await self.fetch_aggregate_events(aggregate_id)
                    logging.info("Processing events: ")
                    logging.info([e.model_dump() for e in events])
                    # Process events under aggregate sequentially
                    for event in events:
                        try:
                            payload = {
                                "event_id": event.id,
                                "event_type": event.event_type,
                                "payload": event.payload,
                            }
                            logging.info("Proessing event: ")
                            logging.info(payload)
                            delivery_future = await self.producer.produce(
                                topic=self.config.topic,
                                key=str(aggregate_id),
                                # TODO Instead of dumping the event dict raw, use a pydantic model or
                                # maybe Apache Avro to control the structure.
                                value=json.dumps(payload, indent=4).encode("utf-8"),
                            )
                            await delivery_future
                            # After delivery mark the event as processed.
                            async with self.session_factory() as session:
                                await session.execute(
                                    update(OutboxEvent)
                                    .where(OutboxEvent.id == event.id)
                                    .values(processed_at=func.now())
                                )
                                await session.commit()
                        except Exception as e:
                            logging.error(f"Failed to deliver event {event.id}")
                            logging.exception(e)
                # Release locks
                if aggregates:
                    await self.release_aggregate_locks(aggregates)

                await asyncio.sleep(0)

            # Gracefully shutdown
            logging.info("Initiating gracefull shutdown")
            # First release the remaining messages to be sent.
            logging.info("Flushing remaining messages")
            await self.producer.flush()
        finally:
            logging.info("Closing the producre")
            await self.producer.close()

    async def lock_aggregates(self) -> list[int]:
        async with self.session_factory() as session:
            stmt = (
                pg_insert(AggregateLock)
                .from_select(
                    [
                        AggregateLock.aggregate_id,
                        AggregateLock.claimed_by,
                        AggregateLock.claimed_at,
                    ],
                    select(
                        OutboxEvent.aggregate_id, literal(self.worker_id), func.now()
                    )
                    .where(OutboxEvent.processed_at.is_(None))
                    .distinct(),
                )
                .on_conflict_do_nothing()
                .returning(AggregateLock.aggregate_id)
            )
            r = await session.execute(stmt)
            r = r.scalars().all()
            await session.commit()
            return r

    async def fetch_aggregate_events(self, aggregate_id: int) -> list[OutboxEventDTO]:
        async with self.session_factory() as session:
            async with session.begin():
                q = select(OutboxEvent).where(
                    OutboxEvent.processed_at.is_(None),
                    OutboxEvent.aggregate_id == aggregate_id,
                )
                r = (await session.scalars(q)).all()
                return [OutboxEventDTO.from_outbox_event_entity(e) for e in r]

    async def release_aggregate_locks(self, aggregates: list[int]):
        async with self.session_factory() as session:
            stmt = (
                delete(AggregateLock)
                .where(AggregateLock.aggregate_id.in_(aggregates))
                .returning(AggregateLock.id, AggregateLock.aggregate_id)
            )
            released_locks = (await session.execute(stmt)).mappings().all()
            await session.commit()
            return released_locks

    async def delete_expired_locks(self) -> list[dict]:
        async with self.session_factory() as session:
            async with session.begin():
                r = await session.execute(
                    delete(AggregateLock)
                    .where(AggregateLock.claimed_at < func.now() - timedelta(seconds=5))
                    .returning(AggregateLock.id, AggregateLock.aggregate_id)
                )
                return r.mappings().all()
