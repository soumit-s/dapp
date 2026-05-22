from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from .db import DB
from .config import load_config
from .services import StoreService

config_singleton = load_config()
db_singleton = DB(url=config_singleton.database_url)


GetConfigDep = Depends(lambda: config_singleton)
GetDbDep = Depends(lambda: db_singleton)


async def get_db() -> DB:
    return db_singleton


async def get_db_async_engine(db: Annotated[DB, GetDbDep]) -> AsyncEngine:
    return db.get_async_engine()


GetDbAsyncEngineDep = Depends(get_db_async_engine)


async def get_db_async_session_factory(
    db: Annotated[DB, GetDbDep],
) -> async_sessionmaker[AsyncSession]:
    return db.get_async_session_factory()


GetDbAsyncSessionFactoryDep = Depends(get_db_async_session_factory)


async def get_db_async_session(
    factory: Annotated[async_sessionmaker[AsyncSession], GetDbAsyncSessionFactoryDep],
):
    async with factory() as session:
        yield session


GetDbAsyncSessionDep = Depends(get_db_async_session)


async def get_store_service(session: Annotated[AsyncSession, GetDbAsyncSessionDep]):
    return StoreService(session)


GetStoreServiceDep = Depends(get_store_service)
