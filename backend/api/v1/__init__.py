from fastapi import APIRouter

from backend.api.v1.auth import router as auth_router
from backend.api.v1.users import router as users_router
from backend.api.v1.properties import router as properties_router
from backend.api.v1.media import router as media_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
v1_router.include_router(properties_router)
v1_router.include_router(media_router)
