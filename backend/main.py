import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.api.v1 import v1_router
from backend.core.config import get_settings
from backend.core.database import Database
from backend.logging.logger import get_logger, setup_logging
from backend.services.auth_service import AuthService
from shared.constants import VERSION

settings = get_settings()
setup_logging(settings.LOG_FILE, settings.LOG_LEVEL)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Starting %s v%s",
        settings.APP_NAME,
        settings.APP_VERSION,
        extra={"extra_data": {"env": settings.ENVIRONMENT}},
    )
    await Database.connect(settings.MONGODB_URI, settings.MONGODB_DB)
    await AuthService().seed_admin()
    yield
    await Database.close()
    logger.info("Application shut down")


app = FastAPI(
    title=settings.APP_NAME,
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        extra={"extra_data": {"path": request.url.path, "method": request.method}},
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url)},
    )


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
