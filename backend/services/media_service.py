from datetime import datetime, timezone
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.config import get_settings
from backend.core.database import Database
from backend.logging.logger import get_logger
from backend.schemas.media import MediaResponse
from backend.storage.file_storage import FileStorage

logger = get_logger(__name__)


class MediaService:
    def __init__(self) -> None:
        self.db: AsyncIOMotorDatabase = Database.get_db()
        self.settings = get_settings()
        self.storage = FileStorage()

    async def upload(
        self,
        file_bytes: bytes,
        filename: str,
        content_type: str,
        uploaded_by: str,
        property_id: str | None = None,
    ) -> MediaResponse:
        ext = Path(filename).suffix.lower()
        is_video = ext in {".mp4", ".mov", ".avi"}
        media_type = "video" if is_video else "photo"

        if is_video:
            max_size = self.settings.MAX_VIDEO_SIZE_MB * 1024 * 1024
        else:
            max_size = self.settings.MAX_PHOTO_SIZE_MB * 1024 * 1024

        if len(file_bytes) > max_size:
            raise ValueError(f"File size exceeds maximum allowed size")

        saved_path, unique_name = await self.storage.save(file_bytes, filename, media_type)

        media_doc = {
            "filename": unique_name,
            "original_name": filename,
            "media_type": media_type,
            "mime_type": content_type,
            "size_bytes": len(file_bytes),
            "file_path": str(saved_path),
            "url": f"/api/v1/media/{unique_name}",
            "property_id": property_id,
            "uploaded_by": uploaded_by,
            "created_at": datetime.now(timezone.utc),
        }

        result = await self.db.media.insert_one(media_doc)
        media_doc["_id"] = str(result.inserted_id)
        logger.info(
            "Media uploaded",
            extra={"extra_data": {"media_id": media_doc["_id"], "type": media_type, "file": filename}},
        )
        return MediaResponse(**media_doc, id=media_doc["_id"])

    async def get_by_filename(self, filename: str) -> MediaResponse | None:
        doc = await self.db.media.find_one({"filename": filename})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return MediaResponse(**doc, id=doc["_id"])

    async def get_by_property(self, property_id: str) -> list[MediaResponse]:
        cursor = self.db.media.find({"property_id": property_id})
        items = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            items.append(MediaResponse(**doc, id=doc["_id"]))
        return items

    async def delete(self, media_id: str) -> None:
        from bson import ObjectId

        doc = await self.db.media.find_one({"_id": ObjectId(media_id)})
        if not doc:
            raise ValueError("Media not found")

        path = Path(doc["file_path"])
        if path.exists():
            path.unlink()

        await self.db.media.delete_one({"_id": ObjectId(media_id)})
        logger.info("Media deleted", extra={"extra_data": {"media_id": media_id}})
