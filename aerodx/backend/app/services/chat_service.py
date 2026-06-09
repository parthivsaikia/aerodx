"""
Chat Service
────────────
Manages multi-turn chat sessions tied (optionally) to scan results.
Replies are rule-based for now — wire up an LLM in _generate_reply()
when you're ready for smarter responses.
"""

import logging
from datetime import datetime

from app.models.schemas import (
    AnalysisResult,
    ChatHistory,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    MessageRole,
)

logger = logging.getLogger(__name__)

# In-memory session store:  session_id → ChatHistory
# Swap for Redis / DB in production
_sessions: dict[str, ChatHistory] = {}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_or_create_session(session_id: str) -> ChatHistory:
    if session_id not in _sessions:
        _sessions[session_id] = ChatHistory(session_id=session_id)
    return _sessions[session_id]


def _generate_reply(
    user_message: str,
    history: list[ChatMessage],
    analysis: AnalysisResult | None,
) -> str:
    """
    Build an assistant reply.

    ┌──────────────────────────────────────────────────────────────────┐
    │  REPLACE THIS with an LLM call (OpenAI, Anthropic, local LLM)  │
    │  when you want smarter conversational responses.                │
    │                                                                  │
    │  You have full context:                                          │
    │    • user_message  – current user input                         │
    │    • history       – ordered list of past ChatMessage objects   │
    │    • analysis      – AnalysisResult for the linked scan (or None)│
    └──────────────────────────────────────────────────────────────────┘
    """
    msg = user_message.lower()

    if analysis:
        label = analysis.predicted_label.value
        conf = f"{analysis.confidence * 100:.1f}%"
        severity = analysis.severity.value

        if any(w in msg for w in ["result", "finding", "diagnosis", "analysis", "what"]):
            findings_text = "\n".join(
                f"  • {f.region}: {f.description} (confidence {f.confidence*100:.0f}%)"
                for f in analysis.findings
            ) or "  • No specific findings recorded."
            recs = "\n".join(f"  {i+1}. {r}" for i, r in enumerate(analysis.recommendations))
            return (
                f"**Analysis Result for scan `{analysis.scan_id}`**\n\n"
                f"- **Predicted condition:** {label}\n"
                f"- **Model confidence:** {conf}\n"
                f"- **Severity:** {severity}\n\n"
                f"**Findings:**\n{findings_text}\n\n"
                f"**Recommendations:**\n{recs}"
            )

        if any(w in msg for w in ["recommend", "next step", "should", "advice"]):
            recs = "\n".join(f"{i+1}. {r}" for i, r in enumerate(analysis.recommendations))
            return f"Based on the scan analysis, here are the recommendations:\n\n{recs}"

        if any(w in msg for w in ["severe", "serious", "critical", "bad"]):
            return (
                f"The detected severity level is **{severity}**. "
                "Please consult a qualified radiologist for a definitive clinical assessment."
            )

        return (
            f"I have the analysis for scan `{analysis.scan_id}`. "
            f"The model detected **{label}** with {conf} confidence. "
            "Ask me about findings, recommendations, or severity for more detail."
        )

    # Generic replies when no scan is linked
    if any(w in msg for w in ["hello", "hi", "hey"]):
        return (
            "Hello! I'm the AeroDx assistant. Upload a CT scan and I can help you "
            "interpret the analysis results, explain findings, and answer questions."
        )

    if any(w in msg for w in ["help", "can you", "what can"]):
        return (
            "I can help you:\n"
            "1. Interpret CT scan analysis results\n"
            "2. Explain detected findings and severity\n"
            "3. Provide recommendations based on the scan\n"
            "4. Generate a downloadable PDF report\n\n"
            "Start by uploading a CT scan image."
        )

    return (
        "I'm here to help you understand your CT scan results. "
        "Please upload a scan or ask me about a specific analysis."
    )


# ── Public API ─────────────────────────────────────────────────────────────────

def process_chat(
    request: ChatRequest,
    analysis: AnalysisResult | None = None,
) -> ChatResponse:
    """Process a user message and return the assistant reply."""
    session = _get_or_create_session(request.session_id)

    # Append user message
    user_msg = ChatMessage(
        role=MessageRole.USER,
        content=request.message,
        scan_id=request.scan_id,
    )
    session.messages.append(user_msg)

    # Generate reply
    reply_text = _generate_reply(request.message, session.messages, analysis)

    # Append assistant message
    assistant_msg = ChatMessage(
        role=MessageRole.ASSISTANT,
        content=reply_text,
        scan_id=request.scan_id,
    )
    session.messages.append(assistant_msg)

    logger.info(
        "Chat [%s] — user: %r | reply: %r",
        request.session_id,
        request.message[:60],
        reply_text[:60],
    )

    return ChatResponse(
        session_id=request.session_id,
        reply=reply_text,
        scan_id=request.scan_id,
        analysis=analysis,
    )


def get_history(session_id: str) -> ChatHistory:
    return _get_or_create_session(session_id)


def clear_session(session_id: str) -> bool:
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False


def list_sessions() -> list[str]:
    return list(_sessions.keys())
