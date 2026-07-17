from sqlalchemy.ext.asyncio.engine import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker


class DB:
    def __init__(self, url: str):
        self.async_engine = create_async_engine(url, plugins=["geoalchemy2"])
        self.async_session_factory = async_sessionmaker(self.async_engine)

    def get_async_engine(self) -> AsyncEngine:
        return self.async_engine

    def get_async_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self.async_session_factory
