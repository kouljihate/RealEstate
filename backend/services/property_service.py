import math
from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import Database
from backend.logging.logger import get_logger
from backend.schemas.property import (
    PaginatedProperties,
    PropertyCreate,
    PropertyResponse,
    PropertyUpdate,
)

logger = get_logger(__name__)


class PropertyService:
    def __init__(self) -> None:
        self.db: AsyncIOMotorDatabase = Database.get_db()

    async def create(self, req: PropertyCreate, owner_id: str) -> PropertyResponse:
        doc = req.model_dump()
        doc["status"] = "available"
        doc["owner_id"] = owner_id
        doc["photos"] = []
        doc["videos"] = []
        doc["is_featured"] = False
        doc["is_published"] = False
        doc["created_at"] = datetime.now(timezone.utc)
        doc["updated_at"] = datetime.now(timezone.utc)

        result = await self.db.properties.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        logger.info("Property created", extra={"extra_data": {"property_id": doc["_id"], "owner": owner_id}})
        return PropertyResponse(**doc, id=doc["_id"])

    async def get_by_id(self, property_id: str) -> PropertyResponse | None:
        doc = await self._find(property_id)
        if not doc:
            return None
        return PropertyResponse(**doc, id=doc["_id"])

    async def update(self, property_id: str, req: PropertyUpdate, user_id: str) -> PropertyResponse:
        doc = await self._find(property_id)
        if not doc:
            raise ValueError("Property not found")
        if doc["owner_id"] != user_id:
            raise PermissionError("Not authorized to update this property")

        update_data = {k: v for k, v in req.model_dump(exclude_none=True).items()}
        update_data["updated_at"] = datetime.now(timezone.utc)

        await self.db.properties.update_one(
            {"_id": ObjectId(property_id)}, {"$set": update_data}
        )
        updated_doc = await self._find(property_id)
        logger.info("Property updated", extra={"extra_data": {"property_id": property_id}})
        return PropertyResponse(**updated_doc, id=updated_doc["_id"])

    async def delete(self, property_id: str, user_id: str) -> None:
        doc = await self._find(property_id)
        if not doc:
            raise ValueError("Property not found")
        if doc["owner_id"] != user_id:
            raise PermissionError("Not authorized to delete this property")

        await self.db.properties.delete_one({"_id": ObjectId(property_id)})
        await self.db.media.delete_many({"property_id": property_id})
        logger.info("Property deleted", extra={"extra_data": {"property_id": property_id}})

    async def list(
        self,
        page: int = 1,
        size: int = 20,
        filters: dict[str, Any] | None = None,
    ) -> PaginatedProperties:
        query = filters or {}
        total = await self.db.properties.count_documents(query)
        pages = math.ceil(total / size) if total > 0 else 0
        skip = (page - 1) * size

        cursor = self.db.properties.find(query).sort("created_at", -1).skip(skip).limit(size)
        items = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            items.append(PropertyResponse(**doc, id=doc["_id"]))

        return PaginatedProperties(
            items=items, total=total, page=page, size=size, pages=pages
        )

    async def add_media_ref(self, property_id: str, media_id: str, media_type: str) -> None:
        field = "videos" if media_type == "video" else "photos"
        await self.db.properties.update_one(
            {"_id": ObjectId(property_id)},
            {"$push": {field: media_id}},
        )

    async def _find(self, property_id: str) -> dict | None:
        try:
            doc = await self.db.properties.find_one({"_id": ObjectId(property_id)})
            if doc:
                doc["_id"] = str(doc["_id"])
            return doc
        except Exception:
            return None
