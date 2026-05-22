from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio.session import async_sessionmaker, AsyncSession

from .db import async_engine, async_session_factory
from .services import *
from .config import Config, config

GetDbAsyncEngineDep = Depends(lambda: async_engine)
GetDbAsyncSessionFactoryDep = Depends(lambda: async_session_factory)


async def get_db_async_session(
    factory: Annotated[async_sessionmaker[AsyncSession], GetDbAsyncSessionFactoryDep],
):
    async with factory() as session:
        yield session


GetDbAsyncSessionDep = Depends(get_db_async_session)

GetConfigDep = Depends(lambda: config)

# redis_service_singleton = RedisService(
#     host=config.redis_host, port=config.redis_port, db=config.redis_db
# )

# GetRedisServiceDep = Depends(lambda: redis_service_singleton)


async def get_jwt_service(config: Annotated[Config, GetConfigDep]):
    return JWTService(config.jwt_secret)


async def get_user_service(session: Annotated[AsyncSession, GetDbAsyncSessionDep]):
    return UserService(session)


GetJwtServiceDep = Depends(get_jwt_service)
GetUserServiceDep = Depends(get_user_service)
