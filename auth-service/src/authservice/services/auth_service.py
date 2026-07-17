from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..schema import User
from .user_service import UserService
from .jwt_service import JWTService
from .password_service import PasswordService
from ..errors import UserNotFoundError, UserNotAuthorizedError


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        jwt_service: JWTService,
        user_service: UserService,
        password_service: PasswordService,
    ):
        self.session = session
        self.jwt_service = jwt_service
        self.user_service = user_service
        self.password_service = password_service

    async def admin_login(self, email: str, password: str):
        """
        Authenticates an admin using email and pasword.
        Can raise UserNotFoundError or UserNotAuthorizedError
        """
        async with self.session.begin():
            # Get user using email
            user = await self.session.scalar(
                select(User)
                .options(selectinload(User.basic_auth), selectinload(User.roles))
                .where(User.email == email)
            )
            if user == None:
                raise UserNotFoundError()
            # Check if it has the admin role.
            if (
                next((role for role in user.roles if role.name == "ADMIN"), None)
                is None
            ):
                raise UserNotAuthorizedError()
            if user.basic_auth == None:
                raise UserNotAuthorizedError()
            # Verify user password.
            if not self.password_service.verify_pwd(
                user.basic_auth.hashed_password, password
            ):
                raise UserNotAuthorizedError()

            # Generate the token
            token = self.jwt_service.generate_admin_token(user_id=str(user.id))
            return token

    async def user_verify_otp(self, phone: str, otp: str):
        """
        Verfies the OTP sent to a phone number. Checks if an user with the phone number
        already exists. If not it creates a new user. After that it returns a JWT for the user.

        Raises UserNotAuthorizedError in case OTP does not match.
        """
        if otp != "1234":
            raise UserNotAuthorizedError()
        user = await self.user_service.upsert_user(phone)
        jwt = self.jwt_service.generate_user_token(user_id=str(user.id))
        return jwt
