from fastapi import APIRouter, HTTPException, status

from app.models.schemas import ChatHistory, ChatRequest, ChatResponse
from app.services import chat_service, scan_service

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "/",
    response_model=ChatResponse,
    summary="Send a message to the AeroDx assistant",
    description=(
        "Optionally attach a `scan_id` to ground the reply in a specific analysis. "
        "If `scan_id` is provided the scan must have been analysed already."
    ),
)
def chat(request: ChatRequest):
    analysis = None
    if request.scan_id:
        try:
            analysis = scan_service.get_scan_result(request.scan_id)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"No analysis found for scan '{request.scan_id}'. "
                    "Run POST /scans/analyze/{scan_id} first."
                ),
            )

    return chat_service.process_chat(request, analysis)


@router.get(
    "/{session_id}/history",
    response_model=ChatHistory,
    summary="Retrieve full chat history for a session",
)
def get_history(session_id: str):
    return chat_service.get_history(session_id)


@router.delete(
    "/{session_id}",
    summary="Clear a chat session",
    status_code=status.HTTP_200_OK,
)
def clear_session(session_id: str):
    deleted = chat_service.clear_session(session_id)
    return {"deleted": deleted, "session_id": session_id}


@router.get(
    "/",
    summary="List active session IDs",
)
def list_sessions():
    return {"sessions": chat_service.list_sessions()}
