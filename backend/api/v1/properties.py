from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.api.deps import get_current_user
from backend.logging.logger import get_logger
from backend.schemas.property import (
    PaginatedProperties,
    PropertyCreate,
    PropertyResponse,
    PropertyUpdate,
)
from backend.schemas.user import UserResponse
from backend.services.property_service import PropertyService

logger = get_logger(__name__)
router = APIRouter(prefix="/properties", tags=["Properties"])


@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    req: PropertyCreate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> PropertyResponse:
    return await PropertyService().create(req, current_user.id)


@router.get("/", response_model=PaginatedProperties)
async def list_properties(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    property_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
) -> PaginatedProperties:
    filters = {}
    if property_type:
        filters["property_type"] = property_type
    if status:
        filters["status"] = status
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        filters["price"] = price_filter
    if city:
        filters["location.city"] = {"$regex": city, "$options": "i"}
    if state:
        filters["location.state"] = {"$regex": state, "$options": "i"}

    return await PropertyService().list(page=page, size=size, filters=filters)


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(property_id: str) -> PropertyResponse:
    prop = await PropertyService().get_by_id(property_id)
    if not prop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return prop


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: str,
    req: PropertyUpdate,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> PropertyResponse:
    try:
        return await PropertyService().update(property_id, req, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: str,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> None:
    try:
        await PropertyService().delete(property_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
