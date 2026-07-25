from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import Database
from backend.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.logging.logger import get_logger
from backend.models.user import User
from backend.schemas.auth import LoginRequest, RegisterRequest
from backend.schemas.user import UserResponse

logger = get_logger(__name__)


class AuthService:
    def __init__(self) -> None:
        self.db: AsyncIOMotorDatabase = Database.get_db()

    async def register(self, req: RegisterRequest) -> UserResponse:
        existing = await self.db.users.find_one(
            {"$or": [{"email": req.email}, {"username": req.username}]}
        )
        if existing:
            logger.warning("Registration conflict", extra={"extra_data": {"email": req.email}})
            raise ValueError("Email or username already registered")

        user_doc = {
            "email": req.email,
            "username": req.username,
            "hashed_password": hash_password(req.password),
            "full_name": req.full_name,
            "phone": req.phone,
            "role": "customer",
            "is_active": True,
            "is_verified": False,
            "avatar_url": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = await self.db.users.insert_one(user_doc)
        user_doc["_id"] = str(result.inserted_id)
        logger.info("User registered", extra={"extra_data": {"user_id": user_doc["_id"], "email": req.email}})
        return UserResponse(**user_doc, id=user_doc["_id"])

    async def login(self, req: LoginRequest) -> dict:
        user_doc = await self.db.users.find_one({"email": req.email})
        if not user_doc or not verify_password(req.password, user_doc["hashed_password"]):
            logger.warning("Login failed", extra={"extra_data": {"email": req.email}})
            raise ValueError("Invalid email or password")

        user_doc["_id"] = str(user_doc["_id"])
        token_data = {"sub": user_doc["_id"], "role": user_doc["role"]}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": user_doc["_id"]})

        logger.info("User logged in", extra={"extra_data": {"user_id": user_doc["_id"]}})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")

        user_id = payload.get("sub")
        user_doc = await self.db.users.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            raise ValueError("User not found")

        new_token_data = {"sub": user_id, "role": user_doc["role"]}
        return {
            "access_token": create_access_token(new_token_data),
            "refresh_token": create_refresh_token({"sub": user_id}),
            "token_type": "bearer",
        }

    async def get_current_user(self, user_id: str) -> UserResponse | None:
        try:
            user_doc = await self.db.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
        if not user_doc:
            return None
        user_doc["_id"] = str(user_doc["_id"])
        return UserResponse(**user_doc, id=user_doc["_id"])

    async def seed_admin(self) -> None:
        existing = await self.db.users.find_one({"role": "admin"})
        if existing:
            return
        from backend.core.config import get_settings
        settings = get_settings()

        admin_doc = {
            "email": settings.ADMIN_EMAIL,
            "username": "admin",
            "hashed_password": hash_password(settings.ADMIN_PASSWORD),
            "full_name": "System Administrator",
            "phone": None,
            "role": "admin",
            "is_active": True,
            "is_verified": True,
            "avatar_url": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = await self.db.users.insert_one(admin_doc)
        logger.info("Admin user seeded", extra={"extra_data": {"id": str(result.inserted_id)}})
