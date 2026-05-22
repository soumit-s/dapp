from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import func, select
from ..schema import User, OutboxEvent
from ..models import UserDTO, UserCreatedOutboxEventPayloadDTO


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_user(self, phone: str) -> UserDTO:
        """
        Creates a new user with the given phone number. If an user already
        exists with the phone number than return the user.
        """
        async with self.session.begin():
            # Check if user already exists with given phone number
            r = await self.session.scalars(select(User).where(User.phone == phone))
            u = r.one_or_none()
            if u != None:
                return UserDTO.from_user_entity(u)
            u = User(phone=phone)
            self.session.add(u)
            # Flush to get the ID.
            await self.session.flush()

            dto = UserDTO.from_user_entity(u)

            outbox_event_payload = UserCreatedOutboxEventPayloadDTO.from_user_model(
                dto
            ).model_dump()
            o = OutboxEvent(
                aggregate_id=u.id,
                event_type="user.created",
                payload=outbox_event_payload,
            )
            self.session.add(o)

            return dto
