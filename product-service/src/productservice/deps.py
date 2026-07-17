from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession

from typing import Annotated

from .service import *
from .errors import AuthError
from .models import JWTPayload, RoleEnum
from .db import DB
from .config import load_config, Config

# Config singleton
config_singleton = load_config()
GetConfigDep = Depends(lambda: config_singleton)

# DB Singleton
db_singleton = DB(url=config_singleton.database_url)
get_db = lambda: db_singleton
GetDbDep = Depends(get_db)


# Auth Service
async def get_auth_service(config: Annotated[Config, GetConfigDep]) -> AuthService:
    return AuthService(config.jwt_secret)


GetAuthServiceDep = Depends(get_auth_service)

# Used for extracting token from X-Authorization: Bearer <token> header
security_scheme = HTTPBearer()


def verify_jwt(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    auth_service: Annotated[AuthService, GetAuthServiceDep],
) -> JWTPayload:
    """
    Verifies JWT and returns its payload. On failure to decode, it raises AuthError.
    """
    jwt = credentials.credentials
    try:
        return auth_service.verify_jwt(jwt)
    except AuthError as e:
        raise e


VerifyJwtDep = Depends(verify_jwt)


def verify_admin(payload: Annotated[JWTPayload, VerifyJwtDep]):
    if payload.audience != RoleEnum.ADMIN:
        raise AuthError("Must be an admin to access this route")
    return payload


VerifyAdminDep = Depends(verify_admin)


def get_admin_user_id(payload: Annotated[JWTPayload, VerifyAdminDep]) -> int:
    return int(payload.subject)


GetAdminUserId = Depends(get_admin_user_id)

GetDbAsyncEngineDep = Depends(lambda: db_singleton.get_async_engine())
GetDbAsyncSessionFactoryDep = Depends(lambda: db_singleton.get_async_session_factory())


async def get_db_async_session(
    factory: Annotated[async_sessionmaker[AsyncSession], GetDbAsyncSessionFactoryDep],
):
    async with factory() as session:
        yield session


GetDbAsyncSessionDep = Depends(get_db_async_session)


def get_product_service(s: Annotated[AsyncSession, GetDbAsyncSessionDep]):
    return ProductService(s)


GetProductServiceDep = Depends(get_product_service)
