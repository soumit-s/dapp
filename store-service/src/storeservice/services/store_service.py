from sqlalchemy.ext.asyncio.session import AsyncSession
from geoalchemy2 import Geography
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin, ST_GeomFromText
from sqlalchemy import select, cast

from ..schema import Store, OutboxEvent
from ..models import CreateStoreDTO, StoreDTO


class StoreService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_store(self, dto: CreateStoreDTO):
        async with self.session.begin():
            coords = None
            if dto.lat and dto.long:
                coords = WKTElement(f"POINT({dto.long} {dto.lat})", srid=4326)
            s = Store(
                name=dto.name,
                description=dto.description,
                coordinates=coords,
                active=False,
            )
            self.session.add(s)
            await self.session.flush()

            dto = StoreDTO.from_store_entity(s)

            aggregate_id = str(s.id)
            aggregate_type = "store"
            event_type = "user.created"
            event = OutboxEvent(
                aggregate_type=aggregate_type,
                aggregate_id=aggregate_id,
                event_type=event_type,
                payload={
                    "aggregate_type": aggregate_type,
                    "aggregate_id": aggregate_id,
                    "event_type": event_type,
                    "payload": dto.model_dump(),
                },
            )
            self.session.add(event)
            return dto

    async def get_stores_in_radius(
        self, lat: float, long: float, radius: float
    ) -> list[StoreDTO]:
        """
        radius: Radius in metres.
        """
        async with self.session.begin():
            stmt = select(Store).where(
                Store.active == True,
                ST_DWithin(
                    cast(Store.coordinates, Geography),
                    ST_GeomFromText(f"POINT({long} {lat})", srid=4326),
                    radius,
                ),
            )
            r = await self.session.scalars(stmt)
            return [StoreDTO.from_store_entity(s) for s in r.all()]
