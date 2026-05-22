from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, JSON, Uuid
from sqlalchemy import text, func
from sqlalchemy.orm import mapped_column, relationship, Mapped
from datetime import datetime
from typing import List, Optional
import uuid


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Product(Base, TimestampMixin):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(
        "product_id", Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column("name", String(511))
    # brief: Mapped[str] = mapped_column("brief", String(1023), server_default=text("''"))
    description: Mapped[str] = mapped_column(
        "description", Text, server_default=text("''")
    )

    images: Mapped[List["ProductImage"]] = relationship(
        back_populates="product", lazy="raise"
    )


class ProductImage(Base, TimestampMixin):
    __tablename__ = "product_images"
    id: Mapped[int] = mapped_column(
        "product_image_id", Integer, primary_key=True, autoincrement=True
    )
    url: Mapped[str] = mapped_column("url", String(511))
    product_id: Mapped[int] = mapped_column(
        "product_id", ForeignKey("products.product_id")
    )
    serial_no: Mapped[int] = mapped_column("serial_no", Integer, unique=True)

    product: Mapped["Product"] = relationship(back_populates="images", lazy="raise")


class OutboxEvent(Base):
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
