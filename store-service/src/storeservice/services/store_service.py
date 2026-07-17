from sqlalchemy.ext.asyncio.session import AsyncSession
from geoalchemy2 import Geography
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin, ST_GeomFromText
from sqlalchemy import select, cast, update, CursorResult

from ..schema import Store, OutboxEvent, StoreStatus
from ..models import CreateStoreDTO, StoreDTO, SearchStoreDTO, UpdateStoreDTO
from ..errors import StoreNotFoundError


class StoreService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_store(self, dto: CreateStoreDTO) -> StoreDTO:
        async with self.session.begin():
            coords = None
            if dto.lat and dto.long:
                coords = WKTElement(f"POINT({dto.long} {dto.lat})", srid=4326)
            s = Store(
                name=dto.name,
                description=dto.description,
                coordinates=coords,
            )
            self.session.add(s)
            await self.session.flush()

            store = StoreDTO.from_store_entity(s)

            # Create the outbox event.
            aggregate_id = str(s.id)
            aggregate_type = "store"
            event_type = "store.created"
            event = OutboxEvent(
                aggregate_type=aggregate_type,
                aggregate_id=aggregate_id,
                event_type=event_type,
                payload={
                    "aggregate_type": aggregate_type,
                    "aggregate_id": aggregate_id,
                    "event_type": event_type,
                    "payload": store.model_dump(),
                },
            )
            self.session.add(event)
            await self.session.flush()

            # Add the event id to the payload.
            event.payload["event_id"] = str(event.id)
            # Save the entity.
            await self.session.flush()

            return store

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
    
    async def get_stores(self) -> list[StoreDTO]:
        async with self.session.begin():
            r = await self.session.scalars(select(Store))
            return [StoreDTO.from_store_entity(entity) for entity in r]
    
    async def get_store_by_id(self, store_id: int) -> StoreDTO | None:
        async with self.session.begin():
            e = await self.session.scalar(select(Store).where(Store.id == store_id))
            if e != None:
                return StoreDTO.from_store_entity(e)
    
    async def search_stores(self, opts: SearchStoreDTO) -> list[StoreDTO]:
        async with self.session.begin():
            stmt = select(Store).where(Store.name.ilike(f"%{opts.search}%"))
            r = await self.session.scalars(stmt)
            return [StoreDTO.from_store_entity(entity) for entity in r]
    
    async def update_store(self, store_id: int, dto: UpdateStoreDTO) -> StoreDTO:
        async with self.session.begin():
            store = await self.session.scalar(select(Store).where(Store.id==store_id))
            if store == None:
                raise StoreNotFoundError(f"Store ID: {store_id} not found")
            # Update the ORM entity.
            store.name = dto.name
            store.description = dto.description
            if dto.lat and dto.long:
                store.coordinates = WKTElement(f"POINT({dto.long} {dto.lat})", srid=4326)
            else:
                store.coordinates = None
            # Save the ORM entity.
            self.session.commit()

            return StoreDTO.from_store_entity(store)
    
    async def update_store_status(self, store_id: int, status: StoreStatus) -> bool:
        async with self.session.begin():
            result: CursorResult = await self.session.execute(update(Store).where(Store.id == store_id).values(status = status))
            if result.rowcount != 1:
                raise StoreNotFoundError(f"Store ID = {store_id} not found")
            # TODO Generate outbox event.
            return True