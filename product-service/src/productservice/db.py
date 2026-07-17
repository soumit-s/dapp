from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)


class DB:
    def __init__(self, url: str):
        self.async_engine = create_async_engine(url)
        self.async_session_factory = async_sessionmaker(
            self.async_engine, expire_on_commit=False
        )

    def get_async_engine(self) -> AsyncEngine:
        return self.async_engine

    def get_async_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self.async_session_factory
