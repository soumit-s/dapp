# Contains ADMIN role routes.
from fastapi import APIRouter, Query, HTTPException, status, Response
from typing import Annotated

from ..deps import GetAdminDep, GetStoreServiceDep
from ..models import *
from ..services import StoreService
from ..errors import StoreNotFoundError
from ..schema import StoreStatus

# GET /api/v1/admin/stores # Get all stores.
# GET /api/v1/admin/stores/:id # Get details of a specific store.
# POST /api/v1/admin/stores # Creates a new store
# POST /api/v1/admin/stores/search # Semantic search over stores.
# PUT /api/v1/admin/stores/:id # Replaces existing store, NOTE: does not change status
# PATCH /api/v1/admin/stores/:id/status


router = APIRouter()


@router.get("/admin/stores")
async def get_stores(
    admin: Annotated[UserDetailsDTO, GetAdminDep],
    store_service: Annotated[StoreService, GetStoreServiceDep],
):
    stores = await store_service.get_stores()
    return GetStoresResponseDTO(stores=stores)


@router.get("/admin/stores/{store_id}")
async def get_store_by_id(
    store_id: int,
    admin: Annotated[UserDetailsDTO, GetAdminDep],
    store_service: Annotated[StoreService, GetStoreServiceDep],
) -> StoreDTO:
    store = await store_service.get_store_by_id(id=store_id)
    if store == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return store


@router.post("/admin/stores")
async def create_store(
    body: CreateStoreDTO,
    admin: Annotated[UserDetailsDTO, GetAdminDep],
    store_service: Annotated[StoreService, GetStoreServiceDep],
) -> StoreDTO:
    store = await store_service.create_store(body)
    return store


@router.post("/admin/stores/search")
async def search_stores(
    body: SearchStoreDTO,
    admin: Annotated[UserDetailsDTO, GetAdminDep],
    store_service: Annotated[StoreService, GetStoreServiceDep],
) -> SearchStoreResponseDTO:
    stores = await store_service.search_stores(body)
    return SearchStoreResponseDTO(stores=stores)


@router.put("/admin/stores/{store_id}")
async def update_store(
    store_id: int,
    body: UpdateStoreDTO,
    admin: Annotated[UserDetailsDTO, GetAdminDep],
    store_service: Annotated[StoreService, GetStoreServiceDep],
) -> StoreDTO:
    try:
        return await store_service.update_store(store_id=store_id, dto=body)
    except StoreNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch("/admin/store/{store_id}/status")
async def update_store_status(
    store_id: int,
    body: UpdateStoreStatusDTO,
    admin: Annotated[UserDetailsDTO, GetAdminDep],
    store_service: Annotated[StoreService, GetStoreServiceDep],
):
    """
    Changes the status of a store.
    200 OK If successfull
    422 UNPROCESSABLE_CONTENT If status cannot be changed due to some business rule
    404 If store could not be found
    400 BAD_REQUEST If there is something wrong with the request syntax
    """
    try:
        ok = await store_service.update_store_status(
            store_id=store_id, status=StoreStatus[body.status]
        )
        if not ok:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
        return Response(status_code=status.HTTP_200_OK)
    except StoreNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
