from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Location(BaseModel):
    address: str
    city: str
    state: str
    country: str
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Property(BaseModel):
    id: str = Field(default=None, alias="_id")
    title: str
    description: str
    price: float
    currency: str = "USD"
    area_hectares: float
    property_type: str
    status: str = "available"
    location: Location
    features: list[str] = []
    soil_type: Optional[str] = None
    water_access: bool = False
    road_access: bool = False
    electricity: bool = False
    photos: list[str] = []
    videos: list[str] = []
    owner_id: str
    is_featured: bool = False
    is_published: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "title": "50 Hectare Organic Farm",
                "description": "Prime farmland with irrigation system...",
                "price": 250000.00,
                "currency": "USD",
                "area_hectares": 50.0,
                "property_type": "farmland",
                "location": {
                    "address": "Km 15 Route de Meknès",
                    "city": "Fès",
                    "state": "Fès-Meknès",
                    "country": "Morocco",
                },
            }
        }
