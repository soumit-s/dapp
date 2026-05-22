from pydantic import BaseModel, Field
from typing import List
from enum import Enum

from .schema import Product

class RoleEnum(str, Enum):
    CUSTOMER="customer"
    ADMIN="admin"
    STORE_CAPTAIN="store_captain"
    DRIVER="driver"

class JWTPayload(BaseModel):
    audience: RoleEnum
    subject: str

class ProductImageDTO(BaseModel):
    serial_no: int
    url: str

class ProductDTO(BaseModel):
    id: int = Field(min=0)
    name: str = Field(min_length=1, strip_whitespace=True)
    description: str = Field(max_length=1023, strip_whitespace=True)
    images: List[ProductImageDTO] = []
    
    @staticmethod
    def from_product_entity(e: Product):
        return ProductDTO(id=e.id, name=e.name, description=e.description)

class UpdateProductDTO(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(min_length=1, strip_whitespace=True)
    description: str = Field(max_length=1023, strip_whitespace=True)

class CreateProductDTO(BaseModel):
    name: str = Field(min_length=1, strip_whitespace=True)
    description: str = ""

class GetProductsDTO(BaseModel):
    total: int
    page: int
    count: int
    products: List[ProductDTO] = []

class GetProductsQueryParamsDTO(BaseModel):
    page: int = Field(ge=0)
    size: int = Field(default=101, min=10, max=100)
