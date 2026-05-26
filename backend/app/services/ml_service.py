"""
ML Model Service
────────────────
This module owns the lifecycle of the ML model.

INTEGRATION GUIDE FOR THE ML TEAM
──────────────────────────────────
1. Drop your trained model file(s) into  /ml_models/
2. In ModelLoader.load()  →  replace the stub with your real loader
   (torch.load / tf.keras.models.load_model / ONNX runtime, etc.)
3. In MLService.predict() →  replace the stub with your real inference call
4. Make sure predict() returns an AnalysisResult with all fields populated.

Everything else (routes, report generation, chat) needs zero changes.
"""

import logging
import uuid
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.models.schemas import (
    AnalysisResult,
    DiseaseLabel,
    Finding,
    SeverityLevel,
)

logger = logging.getLogger(__name__)


# ── Model loader ───────────────────────────────────────────────────────────────

class ModelLoader:
    """Singleton that loads the ML model once at startup."""

    _instance = None
    _model = None
    _loaded: bool = False
    MODEL_VERSION: str = "stub-v0.1"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self) -> bool:
        """
        Load the model from disk.

        ┌──────────────────────────────────────────────────────────┐
        │  REPLACE THIS BLOCK with your real model loading logic.  │
        │                                                          │
        │  Example (PyTorch):                                      │
        │    model_path = settings.ML_MODELS_DIR / "model.pt"     │
        │    self._model = torch.load(model_path)                  │
        │    self._model.eval()                                    │
        │                                                          │
        │  Example (TensorFlow / Keras):                           │
        │    model_path = settings.ML_MODELS_DIR / "model.h5"     │
        │    self._model = tf.keras.models.load_model(model_path) │
        │                                                          │
        │  Example (ONNX):                                         │
        │    import onnxruntime as ort                             │
        │    model_path = settings.ML_MODELS_DIR / "model.onnx"   │
        │    self._model = ort.InferenceSession(str(model_path))  │
        └──────────────────────────────────────────────────────────┘
        """
        try:
            model_files = list(settings.ML_MODELS_DIR.glob("*"))
            if not model_files:
                logger.warning(
                    "No model files found in %s – running with STUB model.",
                    settings.ML_MODELS_DIR,
                )
                self._loaded = True          # stub is always "loaded"
                return True

            # ── REAL LOADING GOES HERE ──────────────────────────────────────
            logger.info("Model file(s) found: %s", [f.name for f in model_files])
            # self._model = <your loader>
            # self.MODEL_VERSION = "1.0.0"
            # ────────────────────────────────────────────────────────────────

            self._loaded = True
            logger.info("Model loaded successfully (version %s)", self.MODEL_VERSION)
            return True

        except Exception as exc:
            logger.exception("Failed to load model: %s", exc)
            self._loaded = False
            return False

    @property
    def model(self):
        return self._model

    @property
    def is_loaded(self) -> bool:
        return self._loaded


# ── Inference service ──────────────────────────────────────────────────────────

class MLService:
    """Runs inference and returns a structured AnalysisResult."""

    def __init__(self):
        self.loader = ModelLoader()

    def predict(self, scan_id: str, image_path: Path) -> AnalysisResult:
        """
        Run the model on a single CT scan image.

        ┌──────────────────────────────────────────────────────────────┐
        │  REPLACE THE STUB BODY with your real inference pipeline.   │
        │                                                              │
        │  Steps you likely need:                                     │
        │   1. Load/decode the image (PIL, SimpleITK, pydicom, etc.)  │
        │   2. Pre-process / normalise / resize                        │
        │   3. Run model.predict() or model(tensor)                    │
        │   4. Post-process logits → probabilities → label             │
        │   5. Fill and return AnalysisResult                          │
        └──────────────────────────────────────────────────────────────┘
        """
        if not self.loader.is_loaded:
            raise RuntimeError("ML model is not loaded.")

        # ── STUB: returns a fixed placeholder result ────────────────────────
        import random
        labels = list(DiseaseLabel)
        predicted = random.choice(labels)
        confidence = round(random.uniform(0.70, 0.99), 4)

        findings = [
            Finding(
                region="Left lower lobe",
                description="Stub finding – replace with real inference output.",
                confidence=round(random.uniform(0.6, 0.95), 4),
            )
        ]

        raw_probs = {label.value: round(random.uniform(0, 1), 4) for label in labels}
        total = sum(raw_probs.values())
        raw_probs = {k: round(v / total, 4) for k, v in raw_probs.items()}

        return AnalysisResult(
            scan_id=scan_id,
            filename=image_path.name,
            predicted_label=predicted,
            confidence=confidence,
            severity=SeverityLevel.MILD,
            findings=findings,
            recommendations=[
                "This is a STUB result. Integrate real model before clinical use.",
                "Consult a qualified radiologist for interpretation.",
            ],
            model_version=self.loader.MODEL_VERSION,
            analyzed_at=datetime.utcnow(),
            raw_probabilities=raw_probs,
        )
        # ── END STUB ────────────────────────────────────────────────────────


# Module-level singletons
model_loader = ModelLoader()
ml_service = MLService()
