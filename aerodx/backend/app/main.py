import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import settings
from app.models.schemas import HealthResponse
from app.routes import chat, reports, scans
from app.services.ml_service import model_loader

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── App factory ────────────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "REST API for AeroDx — AI-powered lung disease detection from CT scans.\n\n"
            "**Workflow:**\n"
            "1. `POST /scans/upload` — upload a CT scan image\n"
            "2. `POST /scans/analyze/{scan_id}` — run ML inference\n"
            "3. `POST /chat/` — chat about the results\n"
            "4. `POST /reports/generate` — download the PDF report\n"
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── Middleware ─────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # ── Routers ────────────────────────────────────────────────────────────────
    app.include_router(scans.router)
    app.include_router(chat.router)
    app.include_router(reports.router)

    # ── Startup / Shutdown ─────────────────────────────────────────────────────
    @app.on_event("startup")
    async def startup():
        logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
        success = model_loader.load()
        if success:
            logger.info("ML model ready.")
        else:
            logger.warning("ML model failed to load — running in stub mode.")

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Shutting down %s", settings.APP_NAME)

    # ── Health check ───────────────────────────────────────────────────────────
    @app.get("/health", response_model=HealthResponse, tags=["Health"])
    def health():
        return HealthResponse(
            status="ok",
            version=settings.APP_VERSION,
            model_loaded=model_loader.is_loaded,
        )

    @app.get("/", tags=["Health"])
    def root():
        return {
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "docs": "/docs",
        }

    return app


app = create_app()
