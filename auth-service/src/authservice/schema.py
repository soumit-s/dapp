from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import DateTime, Integer, ForeignKey, func, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from uuid import uuid4


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime(True), server_default=func.now(), onupdate=func.now()
    )


class SoftDelMixin:
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        "deleted_at", DateTime(True), default=None
    )


class User(Base, TimestampMixin, SoftDelMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, autoincrement=True)
    phone: Mapped[Optional[str]] = mapped_column("phone", String(31))


class OutboxEvent(Base, TimestampMixin):
    __tablename__ = "outbox_events"
    id: Mapped[str] = mapped_column(
        "id", String, primary_key=True, default=str(uuid4())
    )
    aggregate_id: Mapped[int] = mapped_column("aggregate_id", Integer)
    event_type: Mapped[str] = mapped_column("event_type", String)
    payload: Mapped[dict] = mapped_column("payload", JSON)

    processed_at: Mapped[Optional[datetime]] = mapped_column(
        "processed_at", DateTime(True)
    )


class AggregateLock(Base):
    __tablename__ = "aggregate_locks"
    id: Mapped[str] = mapped_column(
        "lock_id", String, primary_key=True, default=str(uuid4())
    )
    aggregate_id: Mapped[int] = mapped_column("aggregate_id", Integer, unique=True)
    claimed_by: Mapped[str] = mapped_column("claimed_by", String)
    claimed_at: Mapped[str] = mapped_column(
        "claimed_at", DateTime(True), server_default=func.now()
    )
