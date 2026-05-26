from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# ── Enums ──────────────────────────────────────────────────────────────────────

class DiseaseLabel(str, Enum):
    NORMAL = "Normal"
    COVID19 = "COVID-19"
    PNEUMONIA = "Pneumonia"
    TUBERCULOSIS = "Tuberculosis"
    LUNG_CANCER = "Lung Cancer"
    FIBROSIS = "Pulmonary Fibrosis"
    UNKNOWN = "Unknown"


class SeverityLevel(str, Enum):
    NONE = "None"
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    CRITICAL = "Critical"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# ── Scan / Analysis schemas ────────────────────────────────────────────────────

class Finding(BaseModel):
    region: str = Field(..., description="Anatomical region, e.g. 'Left lower lobe'")
    description: str = Field(..., description="Free-text radiological finding")
    confidence: float = Field(..., ge=0.0, le=1.0)


class AnalysisResult(BaseModel):
    scan_id: str
    filename: str
    predicted_label: DiseaseLabel
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: SeverityLevel
    findings: list[Finding] = []
    recommendations: list[str] = []
    model_version: str
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)
    raw_probabilities: Optional[dict[str, float]] = None  # label → probability map


class ScanUploadResponse(BaseModel):
    scan_id: str
    filename: str
    file_size_bytes: int
    upload_path: str
    message: str


# ── Chat schemas ───────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    scan_id: Optional[str] = None          # if this message is tied to a scan
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique chat session identifier")
    message: str = Field(..., min_length=1, max_length=4000)
    scan_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    scan_id: Optional[str] = None
    analysis: Optional[AnalysisResult] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistory(BaseModel):
    session_id: str
    messages: list[ChatMessage] = []


# ── Report schemas ─────────────────────────────────────────────────────────────

class PatientInfo(BaseModel):
    name: Optional[str] = "Anonymous"
    age: Optional[int] = None
    gender: Optional[str] = None
    patient_id: Optional[str] = None
    referring_physician: Optional[str] = None


class ReportRequest(BaseModel):
    scan_id: str
    patient_info: Optional[PatientInfo] = None
    include_chat_history: bool = False
    session_id: Optional[str] = None       # required if include_chat_history=True


class ReportResponse(BaseModel):
    scan_id: str
    report_url: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ── Health check ───────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
