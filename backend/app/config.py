from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "AeroDx - Lung Disease Detection API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Storage
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    ML_MODELS_DIR: Path = BASE_DIR / "ml_models"

    # File constraints
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: list[str] = [".png", ".jpg", ".jpeg", ".dcm", ".nii", ".nii.gz"]

    # CORS - add your frontend URL here
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Report config
    REPORT_TITLE: str = "AeroDx Lung Disease Detection Report"
    HOSPITAL_NAME: str = "AeroDx Medical Imaging"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.ML_MODELS_DIR.mkdir(parents=True, exist_ok=True)
