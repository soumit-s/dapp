from fastapi import APIRouter, HTTPException, status, Query
from typing import Annotated

from productservice.models import CreateProductDTO, ProductDTO, UpdateProductDTO
from productservice.models import GetProductsQueryParamsDTO, GetProductsDTO
from productservice.deps import VerifyAdminDep, GetProductServiceDep
from productservice.service import ProductService
from productservice.errors import ProductNotFoundError

router = APIRouter(prefix="/admin", dependencies=[VerifyAdminDep])


@router.get("/product", response_model=GetProductsDTO)
async def get_products(
    filters: Annotated[GetProductsQueryParamsDTO, Query()],
    product_service: Annotated[ProductService, GetProductServiceDep],
):
    return await product_service.get_products(filters)


@router.get("/product/{id}", response_model=ProductDTO)
async def get_product_by_id(
    id: int,
    product_service: Annotated[ProductService, GetProductServiceDep],
):
    try:
        return await product_service.get_product(id)
    except ProductNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/product", response_model=ProductDTO)
async def create_product(
    body: CreateProductDTO,
    product_service: Annotated[ProductService, GetProductServiceDep],
):
    return await product_service.create_product(body)


@router.post("/product/search")
async def search_products():
    pass


@router.put("/product", response_model=ProductDTO)
async def update_product(
    body: UpdateProductDTO,
    product_service: Annotated[ProductService, GetProductServiceDep],
):
    try:
        return await product_service.update_product(body)
    except ProductNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/product/{product_id}/image")
async def add_product_image(product_id: int):
    pass


@router.put("/product/{product_id}/image")
async def replace_product_image(product_id: int):
    pass



# # Contains ADMIN role routes.
# from fastapi import APIRouter, Query
# from typing import Annotated
# from ..models import GetProductsQueryDTO

# # GET /api/v1/admin/products?page=<int>&limit=<int>&sort_by=<created_at, name>&order=<asc, desc>
# # GET /api/v1/admin/products/:id # Get details of a specific product
# # POST /api/v1/admin/products # Creates a new product
# # POST /api/v1/admin/products/search # Semantic search over product
# # PUT /api/v1/admin/products/:id # Replaces existing product

# router = APIRouter()


# @router.get("/admin/products")
# async def get_products(query: Annotated[GetProductsQueryDTO, Query()]):
#     pass

# @router.get("/admin/products/{product_id}")
# async def get_product(product_id: int):
#     pass

# @router.post("/admin/products")
# async def create_product():
#     """
#     Creates a new product
#     """
#     pass

# @router.post("/admin/products/search")
# async def search_products():
#     """
#     Used to search products
#     """
#     pass

# @router.put("/admin/products/{product_id}")
# async def replace_product():
#     pass


# class GetProductsQueryDTO(BaseModel):
#     page: int = Field(ge=1)
#     limit: int = Field(ge=5, le=200)
#     sort_by: Literal["name", "created_at"] | None
#     order: Literal["asc", "desc"] | None