from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.logging.logger import get_logger

logger = get_logger(__name__)


class Database:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

    @classmethod
    async def connect(cls, uri: str, db_name: str) -> None:
        cls.client = AsyncIOMotorClient(uri)
        cls.db = cls.client[db_name]
        await cls.client.admin.command("ping")
        logger.info("Connected to MongoDB", extra={"db": db_name})

    @classmethod
    async def close(cls) -> None:
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        if cls.db is None:
            raise RuntimeError("Database not initialized")
        return cls.db


async def get_database() -> AsyncIOMotorDatabase:
    return Database.get_db()
