from ..models import ProductDTO, CreateProductDTO, UpdateProductDTO
from ..models import GetProductsQueryParamsDTO, GetProductsDTO
from ..schema import Product, OutboxEvent
from ..errors import ProductNotFoundError

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import update, select, func
from sqlalchemy.orm import selectinload


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_product(self, dto: CreateProductDTO) -> ProductDTO:
        async with self.session.begin():
            product = Product(name=dto.name, description=dto.description, images=[])
            self.session.add(product)
            await self.session.flush()

            dto = ProductDTO.from_product_entity(product)

            # Create the outbox event
            outbox_event = self.create_outbox_event("user.created", dto)
            self.session.add(outbox_event)

            return dto

    async def update_product(self, dto: UpdateProductDTO) -> ProductDTO:
        async with self.session.begin():
            p = (
                await self.session.scalars(
                    select(Product)
                    .where(Product.id == dto.id)
                    .options(selectinload(Product.images))
                )
            ).one_or_none()
            if not p:
                raise ProductNotFoundError()
            p.name = dto.name
            p.description = dto.description

            # Flush the changes made to the product.
            await self.session.flush()

            dto = ProductDTO.from_product_entity(p)

            # Create the outbox event.
            outbox_event = self.create_outbox_event("user.updated", dto)
            self.session.add(outbox_event)

            return dto

    async def get_product(self, id: int) -> ProductDTO:
        q = (
            select(Product)
            .where(Product.id == id)
            .options(selectinload(Product.images))
        )
        p = (await self.session.scalars(q)).one_or_none()
        if not p:
            raise ProductNotFoundError()
        return ProductDTO.from_product_entity(p)

    async def get_products(self, filters: GetProductsQueryParamsDTO) -> GetProductsDTO:
        q = (
            select(Product, func.count().over().label("total_count"))
            .options(selectinload(Product.images))
            .offset((filters.page - 1) * filters.size)
            .limit(filters.limit)
        )
        r = (await self.session.execute(q)).all()
        total = 0
        if r:
            total = r[0].total_count
        products = [ProductDTO.from_product_entity(row[0]) for row in r]

        return GetProductsDTO(
            total=total, page=filters.page, count=len(products), products=products
        )

    def create_outbox_event(self, event_type: str, product: ProductDTO):
        payload = {
            "aggregate_type": "product",
            "aggregate_id": product.id,
            "event_type": event_type,
            "payload": product.model_dump(),
        }
        return OutboxEvent(
            event_type=event_type,
            aggregate_id=str(product.id),
            aggregate_type="product",
            payload=payload,
        )

    async def add_product_image(self, product_id: int):
        pass

    async def update_product_image(self, product_id: int, serial_no: int):
        pass

    async def delete_product_image(self, product_id: int, serial_no: int):
        pass
