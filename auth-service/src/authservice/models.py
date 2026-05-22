from pydantic import BaseModel, Field
from datetime import datetime
from typing import Self

from .schema import User, OutboxEvent


class UserDTO(BaseModel):
    id: int
    phone: str | None  # TODO Add E.164 validation

    @classmethod
    def from_user_entity(cls, u: User) -> Self:
        return cls(id=u.id, phone=u.phone)


class SendPhoneOtpDTO(BaseModel):
    phone: str


class VerifyPhoneOtpDTO(BaseModel):
    phone: str
    otp: str = Field(min_length=4, max_length=4)


class UserCreatedOutboxEventPayloadDTO(BaseModel):
    id: int
    phone: str | None  # TODO Add E.164 validation

    @classmethod
    def from_user_model(cls, u: UserDTO) -> Self:
        return cls(id=u.id, phone=u.phone)


class OutboxEventDTO(BaseModel):
    id: str
    aggregate_id: int
    event_type: str
    payload: dict
    processed_at: datetime | None

    @classmethod
    def from_outbox_event_entity(cls, e: OutboxEvent):
        return cls(
            id=e.id,
            aggregate_id=e.aggregate_id,
            event_type=e.event_type,
            payload=e.payload,
            processed_at=e.processed_at,
        )
