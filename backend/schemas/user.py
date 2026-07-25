from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    username: str
    full_name: str
    phone: str | None = None
    role: str
    is_active: bool
    is_verified: bool
    avatar_url: str | None = None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None


class PaginatedUsers(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
