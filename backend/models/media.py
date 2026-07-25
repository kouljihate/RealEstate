from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Media(BaseModel):
    id: str = Field(default=None, alias="_id")
    filename: str
    original_name: str
    media_type: str
    mime_type: str
    size_bytes: int
    file_path: str
    url: str
    property_id: Optional[str] = None
    uploaded_by: str
    width: Optional[int] = None
    height: Optional[int] = None
    duration_seconds: Optional[float] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True
