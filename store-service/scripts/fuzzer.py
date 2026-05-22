import json
import asyncio
from sqlalchemy import text
from dotenv import load_dotenv
load_dotenv()

from src.storeservice.services import StoreService
from src.storeservice.models import CreateStoreDTO
from src.storeservice.schema import Base 
from src.storeservice.config import load_config
from src.storeservice.db import DB

class Fuzzer:
    def __init__(self, store_service: StoreService):
        self.store_service = store_service
        data = json.load(open("dummy/data.json"))
        self.stores = [CreateStoreDTO.model_validate(s) for s in data]
    
    async def fuzz(self):
        for store in self.stores:
            await self.store_service.create_store(store)
        pass


async def main():
    config  = load_config()
    db = DB(config.database_url)
    async with db.get_async_engine().begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        await conn.run_sync(Base.metadata.create_all)
    session_factory = db.get_async_session_factory()
    async with session_factory() as session:
        store_service = StoreService(session)
        fuzzer = Fuzzer(store_service)
        await fuzzer.fuzz()

if __name__ == "__main__":
    asyncio.run(main())