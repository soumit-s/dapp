from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import func, text
from sqlalchemy import DateTime, Integer, String, Boolean, Uuid, JSON
from typing import Optional
from datetime import datetime
from geoalchemy2 import Geometry

import uuid


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime(True), server_default=func.now(), onupdate=func.now()
    )


class Store(Base, TimestampMixin):
    __tablename__ = "stores"
    id: Mapped[int] = mapped_column(
        "store_id", Integer, primary_key=True, autoincrement=True
    )
    active: Mapped[bool] = mapped_column("active", Boolean)

    name: Mapped[str] = mapped_column("name", String)
    description: Mapped[str] = mapped_column(
        "description", String(511), default=text("''")
    )

    coordinates: Mapped[Optional[Geometry]] = mapped_column(
        "coordinates", Geometry(geometry_type="POINT", srid=4326)
    )


class OutboxEvent(Base, TimestampMixin):
    __tablename__ = "outbox_events"
    id: Mapped[uuid.UUID] = mapped_column(
        "event_id", Uuid, primary_key=True, default=uuid.uuid4
    )
    aggregate_type: Mapped[str] = mapped_column("aggregate_type", String)
    aggregate_id: Mapped[str] = mapped_column("aggregate_id", String)
    event_type: Mapped[str] = mapped_column("event_type", String)
    payload: Mapped[dict] = mapped_column("payload", JSON)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(True), server_default=func.now()
    )
