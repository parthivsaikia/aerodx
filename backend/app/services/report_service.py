"""
Report Service
──────────────
Generates a structured PDF report for a given scan analysis.
Uses ReportLab — no LaTeX dependency needed.
"""

import io
import logging
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.config import settings
from app.models.schemas import AnalysisResult, ChatHistory, PatientInfo, SeverityLevel

logger = logging.getLogger(__name__)

# ── Colour palette ─────────────────────────────────────────────────────────────
PRIMARY = colors.HexColor("#1A3C5E")      # deep navy
ACCENT = colors.HexColor("#2E86C1")       # bright blue
LIGHT_BG = colors.HexColor("#EBF5FB")    # pale blue fill
SEVERITY_COLORS = {
    SeverityLevel.NONE: colors.HexColor("#27AE60"),
    SeverityLevel.MILD: colors.HexColor("#F39C12"),
    SeverityLevel.MODERATE: colors.HexColor("#E67E22"),
    SeverityLevel.SEVERE: colors.HexColor("#E74C3C"),
    SeverityLevel.CRITICAL: colors.HexColor("#922B21"),
}


# ── Style helpers ──────────────────────────────────────────────────────────────

def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=base["Title"],
            fontSize=22,
            textColor=PRIMARY,
            spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=11,
            textColor=ACCENT,
            spaceAfter=2,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontSize=13,
            textColor=PRIMARY,
            fontName="Helvetica-Bold",
            spaceBefore=12,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=10,
            leading=15,
            spaceAfter=4,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["Normal"],
            fontSize=8,
            textColor=colors.grey,
        ),
        "finding": ParagraphStyle(
            "Finding",
            parent=base["Normal"],
            fontSize=10,
            leading=14,
            leftIndent=12,
            spaceAfter=3,
        ),
        "disclaimer": ParagraphStyle(
            "Disclaimer",
            parent=base["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#7F8C8D"),
            leading=12,
        ),
    }


def _divider():
    return HRFlowable(width="100%", thickness=1, color=ACCENT, spaceAfter=6, spaceBefore=4)


# ── Report builder ─────────────────────────────────────────────────────────────

def generate_report(
    analysis: AnalysisResult,
    patient: PatientInfo | None = None,
    chat_history: ChatHistory | None = None,
    scan_image_path: Path | None = None,
) -> bytes:
    """Return the PDF as raw bytes."""

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title=settings.REPORT_TITLE,
    )

    s = _styles()
    story = []
    patient = patient or PatientInfo()

    # ── Header ──────────────────────────────────────────────────────────────
    story.append(Paragraph(settings.HOSPITAL_NAME, s["subtitle"]))
    story.append(Paragraph(settings.REPORT_TITLE, s["title"]))
    story.append(Spacer(1, 2 * mm))
    story.append(_divider())

    # ── Meta table ───────────────────────────────────────────────────────────
    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    meta_data = [
        ["Scan ID", analysis.scan_id, "Generated", generated_at],
        ["Patient Name", patient.name or "—", "Model Version", analysis.model_version],
        ["Patient ID", patient.patient_id or "—", "Filename", analysis.filename],
        ["Referring Physician", patient.referring_physician or "—", "Analysed At",
         analysis.analyzed_at.strftime("%Y-%m-%d %H:%M UTC")],
    ]
    if patient.age or patient.gender:
        meta_data.append([
            "Age / Gender",
            f"{patient.age or '—'} / {patient.gender or '—'}",
            "", ""
        ])

    meta_table = Table(meta_data, colWidths=[45 * mm, 55 * mm, 40 * mm, 50 * mm])
    meta_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, LIGHT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4 * mm))

    # ── Scan image (optional) ────────────────────────────────────────────────
    if scan_image_path and scan_image_path.exists():
        suffix = scan_image_path.suffix.lower()
        if suffix in {".png", ".jpg", ".jpeg"}:
            try:
                img = Image(str(scan_image_path), width=80 * mm, height=80 * mm)
                img.hAlign = "CENTER"
                story.append(Paragraph("CT Scan Image", s["section"]))
                story.append(_divider())
                story.append(img)
                story.append(Spacer(1, 4 * mm))
            except Exception as exc:
                logger.warning("Could not embed scan image: %s", exc)

    # ── Primary result ───────────────────────────────────────────────────────
    story.append(Paragraph("Diagnosis Summary", s["section"]))
    story.append(_divider())

    sev_color = SEVERITY_COLORS.get(analysis.severity, colors.grey)
    result_data = [
        ["Predicted Condition", analysis.predicted_label.value],
        ["Confidence Score", f"{analysis.confidence * 100:.1f}%"],
        ["Severity Level", analysis.severity.value],
    ]
    result_table = Table(result_data, colWidths=[70 * mm, 110 * mm])
    result_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BG),
        ("BACKGROUND", (0, 1), (-1, 1), colors.white),
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_BG),
        ("TEXTCOLOR", (1, 2), (1, 2), sev_color),
        ("FONTNAME", (1, 2), (1, 2), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 4 * mm))

    # ── Findings ─────────────────────────────────────────────────────────────
    if analysis.findings:
        story.append(Paragraph("Radiological Findings", s["section"]))
        story.append(_divider())
        for idx, finding in enumerate(analysis.findings, 1):
            story.append(Paragraph(
                f"<b>{idx}. {finding.region}</b> "
                f"<font color='#7F8C8D'>(confidence: {finding.confidence*100:.0f}%)</font>",
                s["finding"],
            ))
            story.append(Paragraph(finding.description, s["finding"]))
            story.append(Spacer(1, 2 * mm))

    # ── Probability breakdown ─────────────────────────────────────────────────
    if analysis.raw_probabilities:
        story.append(Paragraph("Model Probability Breakdown", s["section"]))
        story.append(_divider())
        sorted_probs = sorted(
            analysis.raw_probabilities.items(), key=lambda x: x[1], reverse=True
        )
        prob_data = [["Condition", "Probability"]] + [
            [label, f"{prob * 100:.2f}%"] for label, prob in sorted_probs
        ]
        prob_table = Table(prob_data, colWidths=[100 * mm, 80 * mm])
        prob_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(prob_table)
        story.append(Spacer(1, 4 * mm))

    # ── Recommendations ───────────────────────────────────────────────────────
    if analysis.recommendations:
        story.append(Paragraph("Recommendations", s["section"]))
        story.append(_divider())
        for i, rec in enumerate(analysis.recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", s["body"]))

    # ── Chat history (optional) ───────────────────────────────────────────────
    if chat_history and chat_history.messages:
        story.append(Spacer(1, 6 * mm))
        story.append(Paragraph("Consultation Chat History", s["section"]))
        story.append(_divider())
        for msg in chat_history.messages:
            role_label = "Patient / User" if msg.role.value == "user" else "AeroDx Assistant"
            ts = msg.timestamp.strftime("%H:%M")
            story.append(Paragraph(
                f"<b>{role_label}</b> <font color='#7F8C8D'>[{ts}]</font>",
                s["body"],
            ))
            story.append(Paragraph(msg.content, s["finding"]))
            story.append(Spacer(1, 2 * mm))

    # ── Disclaimer ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8 * mm))
    story.append(_divider())
    story.append(Paragraph(
        "⚠️  DISCLAIMER: This report is generated by an AI-powered system and is intended "
        "for informational and research purposes only. It does NOT constitute a medical "
        "diagnosis. Always consult a qualified radiologist or physician for clinical "
        "interpretation and treatment decisions.",
        s["disclaimer"],
    ))

    doc.build(story)
    return buffer.getvalue()


def save_report(scan_id: str, pdf_bytes: bytes) -> Path:
    """Persist the PDF to disk and return the path."""
    reports_dir = settings.UPLOAD_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    dest = reports_dir / f"report_{scan_id}.pdf"
    dest.write_bytes(pdf_bytes)
    logger.info("Report saved → %s", dest)
    return dest
