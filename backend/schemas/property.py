from datetime import datetime

from pydantic import BaseModel

from backend.models.property import Location


class PropertyCreate(BaseModel):
    title: str
    description: str
    price: float
    currency: str = "USD"
    area_hectares: float
    property_type: str
    location: Location
    features: list[str] = []
    soil_type: str | None = None
    water_access: bool = False
    road_access: bool = False
    electricity: bool = False


class PropertyUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    currency: str | None = None
    area_hectares: float | None = None
    property_type: str | None = None
    status: str | None = None
    location: Location | None = None
    features: list[str] | None = None
    soil_type: str | None = None
    water_access: bool | None = None
    road_access: bool | None = None
    electricity: bool | None = None
    is_featured: bool | None = None
    is_published: bool | None = None


class PropertyResponse(BaseModel):
    id: str
    title: str
    description: str
    price: float
    currency: str
    area_hectares: float
    property_type: str
    status: str
    location: Location
    features: list[str]
    soil_type: str | None = None
    water_access: bool
    road_access: bool
    electricity: bool
    photos: list[str]
    videos: list[str]
    owner_id: str
    is_featured: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime


class PaginatedProperties(BaseModel):
    items: list[PropertyResponse]
    total: int
    page: int
    size: int
    pages: int
