from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from typing import Optional
from ..schema import User, OutboxEvent, Role, BasicAuth
from ..models import UserDTO, UserCreatedOutboxEventPayloadDTO, AdminUserDTO
from ..config import Config
from ..errors import EmailAlreadyTakenError, RoleAlreadyExistsError


class UserService:
    def __init__(self, session: AsyncSession, config: Config):
        self.session = session
        self.config = config

    async def _get_role(self, role_name: str) -> Optional[Role]:
        """Returns the role entity with the given name, None otherwise."""
        stmt = select(Role).where(Role.name == role_name)
        return await self.session.scalar(stmt)

    async def upsert_user(self, phone: str) -> UserDTO:
        """
        Creates a new user with the given phone number. If an user already
        exists with the phone number than return the user.
        """
        async with self.session.begin():
            # Check if user already exists with given phone number
            r = await self.session.scalars(
                select(User)
                .options(selectinload(User.roles))
                .where(User.phone == phone)
            )
            u = r.one_or_none()
            if u != None:
                return UserDTO.from_user_entity(u)

            # Get the user role.
            user_role = await self._get_role(self.config.role_name_user)
            if user_role is None:
                raise RuntimeError(
                    f"Fatal error: user role not found how is this possible (name = {self.user_role_name})"
                )

            # Create the user entity.
            u = User(phone=phone)
            u.roles.append(user_role)

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

    async def find_user_by_email(self, email: str) -> Optional[User]:
        return (
            await self.session.execute(select(User).where(User.email == email))
        ).one_or_none()

    async def create_admin(self, email: str, hashed_password: str) -> AdminUserDTO:
        """
        Creates an admin user. If user already exists with the given email, then
        it raises EmailAlreadyTakenError.

        """
        async with self.session.begin():
            # Get the admin role
            admin_role = await self._get_role(self.config.role_name_admin)
            if admin_role == None:
                raise RuntimeError(
                    f"Fatal Error: Could not find admin role ({self.config.role_name_admin})"
                )

            # Check if an user with the email is already present
            if (await self.find_user_by_email(email)) != None:
                raise EmailAlreadyTakenError()

            # Create the entity.
            user = User()
            user.email = email
            user.basic_auth = BasicAuth(hashed_password=hashed_password)
            user.roles.append(admin_role)

            self.session.add(user)
            await self.session.flush()

            # Convert entity to user DTO.
            dto = AdminUserDTO.from_user_entity(user)
            # Create the outbox event.
            o = OutboxEvent()
            o.aggregate_id = dto.id
            o.event_type = "user.created"
            o.payload = UserCreatedOutboxEventPayloadDTO.from_user_model(
                dto
            ).model_dump()
            self.session.add(o)

            return dto

    async def create_role(self, name: str) -> int:
        """
        Creates a role with the given name. If role already exists then
        raises RoleAlreadyExistsError
        """
        async with self.session.begin():
            r = await self.session.scalar(select(Role).where(Role.name == name))
            if r != None:
                raise RoleAlreadyExistsError()
            r = Role(name=name)
            self.session.add(r)
            await self.session.commit()

            return r.id
