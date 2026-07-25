from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "RealEstate"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB: str = "realestate"

    SECRET_KEY: str = "change-me-to-a-random-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ADMIN_EMAIL: str = "admin@realestate.com"
    ADMIN_PASSWORD: str = "Admin@123456"

    MEDIA_STORAGE: str = "local"
    MEDIA_PATH: str = "./media"
    MAX_PHOTO_SIZE_MB: int = 10
    MAX_VIDEO_SIZE_MB: int = 100
    ALLOWED_PHOTO_TYPES: str = "jpg,jpeg,png,webp"
    ALLOWED_VIDEO_TYPES: str = "mp4,mov,avi"

    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_BYTES: int = 10_485_760
    LOG_BACKUP_COUNT: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
