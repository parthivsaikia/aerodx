from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse

from app.models.schemas import AnalysisResult, ScanUploadResponse
from app.services import scan_service

router = APIRouter(prefix="/scans", tags=["Scans"])


@router.post(
    "/upload",
    response_model=ScanUploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a CT scan image",
    description=(
        "Upload a CT scan (PNG / JPG / DICOM / NIfTI). "
        "Returns a `scan_id` to use for analysis and report generation."
    ),
)
async def upload_scan(file: UploadFile = File(...)):
    return await scan_service.save_scan(file)


@router.post(
    "/analyze/{scan_id}",
    response_model=AnalysisResult,
    summary="Run ML inference on an uploaded scan",
)
async def analyze_scan(scan_id: str):
    return await scan_service.analyze_scan(scan_id)


@router.get(
    "/{scan_id}/result",
    response_model=AnalysisResult,
    summary="Retrieve cached analysis result",
)
def get_result(scan_id: str):
    return scan_service.get_scan_result(scan_id)


@router.get(
    "/",
    response_model=list[AnalysisResult],
    summary="List all analysed scans",
)
def list_scans():
    return scan_service.list_scans()
