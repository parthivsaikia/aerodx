"""
Scan Service
────────────
Handles file validation, storage, and triggers ML inference.
Results are cached in memory (replace with a DB in production).
"""

import logging
import uuid
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.config import settings
from app.models.schemas import AnalysisResult, ScanUploadResponse
from app.services.ml_service import ml_service

logger = logging.getLogger(__name__)

# In-memory store:  scan_id → AnalysisResult
# Replace with SQLAlchemy / MongoDB / Redis in production
_scan_store: dict[str, AnalysisResult] = {}
_path_store: dict[str, Path] = {}          # scan_id → saved file path


# ── Helpers ────────────────────────────────────────────────────────────────────

def _validate_extension(filename: str) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=(
                f"File type '{suffix}' is not supported. "
                f"Allowed: {settings.ALLOWED_EXTENSIONS}"
            ),
        )


def _validate_size(size: int) -> None:
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if size > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB} MB.",
        )


# ── Public API ─────────────────────────────────────────────────────────────────

async def save_scan(file: UploadFile) -> ScanUploadResponse:
    """Validate, persist, and return upload metadata."""
    _validate_extension(file.filename or "")

    content = await file.read()
    _validate_size(len(content))

    scan_id = str(uuid.uuid4())
    suffix = Path(file.filename).suffix.lower()
    dest_path = settings.UPLOAD_DIR / f"{scan_id}{suffix}"

    async with aiofiles.open(dest_path, "wb") as f:
        await f.write(content)

    _path_store[scan_id] = dest_path
    logger.info("Saved scan %s → %s (%d bytes)", scan_id, dest_path, len(content))

    return ScanUploadResponse(
        scan_id=scan_id,
        filename=file.filename or dest_path.name,
        file_size_bytes=len(content),
        upload_path=str(dest_path),
        message="Scan uploaded successfully. Call /analyze/{scan_id} to run inference.",
    )


async def analyze_scan(scan_id: str) -> AnalysisResult:
    """Run ML inference on a previously uploaded scan."""
    if scan_id in _scan_store:
        logger.info("Returning cached result for scan %s", scan_id)
        return _scan_store[scan_id]

    image_path = _path_store.get(scan_id)
    if image_path is None or not image_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan '{scan_id}' not found. Upload it first via POST /scans/upload.",
        )

    try:
        result = ml_service.predict(scan_id=scan_id, image_path=image_path)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        )

    _scan_store[scan_id] = result
    return result


def get_scan_result(scan_id: str) -> AnalysisResult:
    """Retrieve a cached analysis result."""
    result = _scan_store.get(scan_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analysis found for scan '{scan_id}'. Run POST /scans/analyze/{scan_id} first.",
        )
    return result


def get_scan_path(scan_id: str) -> Path:
    """Return the filesystem path for a scan (used by report service)."""
    path = _path_store.get(scan_id)
    if path is None or not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan file for '{scan_id}' not found.",
        )
    return path


def list_scans() -> list[AnalysisResult]:
    return list(_scan_store.values())
