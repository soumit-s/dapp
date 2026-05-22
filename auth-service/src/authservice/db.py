from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import config

async_engine = create_async_engine(config.database_url)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)