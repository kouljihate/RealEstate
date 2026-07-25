import math
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.api.deps import get_admin_user, get_current_user
from backend.core.database import Database
from backend.logging.logger import get_logger
from backend.schemas.user import PaginatedUsers, UserResponse, UserUpdateRequest

logger = get_logger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=PaginatedUsers)
async def list_users(
    admin: Annotated[UserResponse, Depends(get_admin_user)],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PaginatedUsers:
    db = Database.get_db()
    skip = (page - 1) * size
    total = await db.users.count_documents({})
    pages = math.ceil(total / size) if total > 0 else 0

    cursor = db.users.find({}).sort("created_at", -1).skip(skip).limit(size)
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        items.append(UserResponse(**doc, id=doc["_id"]))

    return PaginatedUsers(items=items, total=total, page=page, size=size, pages=pages)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    admin: Annotated[UserResponse, Depends(get_admin_user)],
) -> UserResponse:
    db = Database.get_db()
    try:
        doc = await db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID")

    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    doc["_id"] = str(doc["_id"])
    return UserResponse(**doc, id=doc["_id"])
