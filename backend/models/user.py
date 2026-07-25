from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: str = Field(default=None, alias="_id")
    email: EmailStr
    username: str
    hashed_password: str
    full_name: str
    phone: Optional[str] = None
    role: str = "customer"
    is_active: bool = True
    is_verified: bool = False
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email": "farmer@example.com",
                "username": "farmer1",
                "full_name": "John Farmer",
                "phone": "+212600000000",
                "role": "customer",
            }
        }
