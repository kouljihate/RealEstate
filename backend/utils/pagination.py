import math
from typing import Any

from motor.motor_asyncio import AsyncIOMotorCursor


async def paginate(
    cursor: AsyncIOMotorCursor,
    total: int,
    page: int,
    size: int,
    serializer: Any,
) -> dict:
    pages = math.ceil(total / size) if total > 0 else 0
    items = []
    async for doc in cursor:
        items.append(serializer(doc))
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
    }
