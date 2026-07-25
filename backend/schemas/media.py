from datetime import datetime

from pydantic import BaseModel


class MediaResponse(BaseModel):
    id: str
    filename: str
    original_name: str
    media_type: str
    mime_type: str
    size_bytes: int
    url: str
    property_id: str | None = None
    uploaded_by: str
    created_at: datetime
