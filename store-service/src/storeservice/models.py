from pydantic import BaseModel, Field
from typing import Self, Literal, Set
from enum import StrEnum
from geoalchemy2.shape import to_shape

from .schema import Store

class UserRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"

class UserDetailsDTO(BaseModel):
    user_id: int
    roles: Set[UserRole]

class CreateStoreDTO(BaseModel):
    name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    description: str = Field(max_length=511, strip_whitespace=True, default="")

    lat: float | None = Field(ge=-90, le=90)
    long: float | None = Field(ge=-180, le=180)

class StoreDTO(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    description: str = Field(max_length=511, strip_whitespace=True, default="")

    lat: float | None = Field(ge=-90, le=90)
    long: float | None = Field(ge=-180, le=180)

    @classmethod
    def from_store_entity(cls, s: Store) -> Self:
        lat, long = None, None
        coords = to_shape(s.coordinates).coords
        if coords:
            lat, long = coords[0]
        return cls(id=s.id, name=s.name, description=s.description, lat=lat, long=long)
    

class GetStoresResponseDTO(BaseModel):
    stores: list[StoreDTO]

class SearchStoreDTO(BaseModel):
    search: str

class SearchStoreResponseDTO(BaseModel):
    stores: list[StoreDTO]

class UpdateStoreDTO(BaseModel):
    name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    description: str = Field(max_length=511, strip_whitespace=True, default="")

    lat: float | None = Field(ge=-90, le=90)
    long: float | None = Field(ge=-180, le=180)

class UpdateStoreStatusDTO(BaseModel):
    status: Literal["INACTIVE", "CLOSED", "OPEN"]