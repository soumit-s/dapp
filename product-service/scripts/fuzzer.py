import json
import asyncio
from dotenv import load_dotenv

load_dotenv()

from src.productservice.models import CreateProductDTO
from src.productservice.schema import Base
from src.productservice.service import ProductService
from src.productservice.config import load_config
from src.productservice.db import DB


class Fuzzer:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service

    async def fuzz(self):
        products = json.load(open("./dummy/products.json"))
        for product in products:
            dto = CreateProductDTO.model_validate(product)
            await self.product_service.create_product(dto)


async def main():
    config = load_config()
    db = DB(config.database_url)
    async with db.get_async_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = db.get_async_session_factory()
    async with session_factory() as session:
        product_service = ProductService(session)
        await Fuzzer(product_service).fuzz()
    pass


if __name__ == "__main__":
    asyncio.run(main())
