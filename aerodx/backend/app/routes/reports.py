from fastapi import APIRouter, status
from fastapi.responses import Response

from app.models.schemas import PatientInfo, ReportRequest
from app.services import chat_service, report_service, scan_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post(
    "/generate",
    summary="Generate a PDF report for a scan",
    description=(
        "Generates a full PDF report including diagnosis, findings, probability breakdown, "
        "and optionally the chat history. Returns the PDF as a binary download."
    ),
    response_class=Response,
    responses={
        200: {
            "content": {"application/pdf": {}},
            "description": "PDF report file",
        }
    },
)
def generate_report(request: ReportRequest):
    # Fetch analysis (raises 404 if not found)
    analysis = scan_service.get_scan_result(request.scan_id)

    # Optionally fetch scan image for embedding
    try:
        scan_path = scan_service.get_scan_path(request.scan_id)
    except Exception:
        scan_path = None

    # Optionally fetch chat history
    chat_history = None
    if request.include_chat_history and request.session_id:
        chat_history = chat_service.get_history(request.session_id)

    pdf_bytes = report_service.generate_report(
        analysis=analysis,
        patient=request.patient_info,
        chat_history=chat_history,
        scan_image_path=scan_path,
    )

    report_service.save_report(request.scan_id, pdf_bytes)

    filename = f"aerodx_report_{request.scan_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        status_code=status.HTTP_200_OK,
    )
