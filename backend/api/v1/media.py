from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from fastapi.responses import FileResponse

from backend.api.deps import get_current_user
from backend.logging.logger import get_logger
from backend.schemas.media import MediaResponse
from backend.schemas.user import UserResponse
from backend.services.media_service import MediaService
from backend.services.property_service import PropertyService
from backend.storage.file_storage import FileStorage
from shared.constants import ALLOWED_PHOTO_EXTENSIONS, ALLOWED_VIDEO_EXTENSIONS

logger = get_logger(__name__)
router = APIRouter(prefix="/media", tags=["Media"])


@router.post("/upload", response_model=MediaResponse, status_code=status.HTTP_201_CREATED)
async def upload_media(
    file: Annotated[UploadFile, File(...)],
    current_user: Annotated[UserResponse, Depends(get_current_user)],
    property_id: str = Form(None),
) -> MediaResponse:
    ext = Path(file.filename).suffix.lower() if file.filename else ""

    if ext in ALLOWED_PHOTO_EXTENSIONS or ext in ALLOWED_VIDEO_EXTENSIONS:
        pass
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '{ext}' not allowed. Allowed: {ALLOWED_PHOTO_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS}",
        )

    file_bytes = await file.read()
    try:
        media = await MediaService().upload(
            file_bytes=file_bytes,
            filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
            uploaded_by=current_user.id,
            property_id=property_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if property_id:
        media_type = "video" if ext in ALLOWED_VIDEO_EXTENSIONS else "photo"
        await PropertyService().add_media_ref(property_id, media.id, media_type)

    return media


@router.get("/{filename}", response_class=FileResponse)
async def get_media(filename: str) -> FileResponse:
    media = await MediaService().get_by_filename(filename)
    if not media:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")

    file_path = Path(media.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found on disk")

    return FileResponse(path=file_path, media_type=media.mime_type, filename=media.original_name)
