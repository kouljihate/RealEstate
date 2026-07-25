import uuid
from pathlib import Path

import aiofiles

from backend.core.config import get_settings
from backend.logging.logger import get_logger

logger = get_logger(__name__)


class FileStorage:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_path = Path(self.settings.MEDIA_PATH)

    async def save(self, file_bytes: bytes, original_name: str, media_type: str) -> tuple[Path, str]:
        ext = Path(original_name).suffix or ".bin"
        unique_name = f"{uuid.uuid4().hex}{ext}"

        sub_dir = "videos" if media_type == "video" else "photos"
        dest_dir = self.base_path / sub_dir
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / unique_name
        async with aiofiles.open(dest_path, "wb") as f:
            await f.write(file_bytes)

        logger.debug("File saved", extra={"extra_data": {"path": str(dest_path), "size": len(file_bytes)}})
        return dest_path, unique_name

    async def read(self, filename: str, media_type: str) -> bytes | None:
        sub_dir = "videos" if media_type == "video" else "photos"
        file_path = self.base_path / sub_dir / filename

        if not file_path.exists():
            return None

        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()

    async def delete(self, filename: str, media_type: str) -> bool:
        sub_dir = "videos" if media_type == "video" else "photos"
        file_path = self.base_path / sub_dir / filename

        if file_path.exists():
            file_path.unlink()
            logger.debug("File deleted", extra={"extra_data": {"path": str(file_path)}})
            return True
        return False
