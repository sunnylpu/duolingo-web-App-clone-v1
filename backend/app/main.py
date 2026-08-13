from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import settings
from app.shared.database import init_db, get_db
from app.shared.logging import setup_logging
from app.shared.middleware import setup_middleware
from app.shared.errors import setup_exception_handlers
from app.api.v1.router import api_v1_router

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events lifecycle manager."""
    logger.info(f"Starting {settings.APP_NAME} service...")
    # Initialize database schemas
    init_db()
    logger.info("Database schemas initialized.")
    yield
    logger.info(f"Shutting down {settings.APP_NAME} service...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Scalable full-stack Duolingo-style language learning platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure middleware & exception handlers
setup_middleware(app)
setup_exception_handlers(app)


# Standard & Kubernetes Liveness Probe
@app.get("/health", tags=["System"], summary="Application health status")
@app.get("/health/live", tags=["System"], summary="Liveness probe")
def liveness_check():
    """Returns operational process liveness status."""
    return {"status": "ok"}


# Kubernetes Readiness Probe
@app.get("/health/ready", tags=["System"], summary="Readiness probe")
def readiness_check(response: Response, db: Session = Depends(get_db)):
    """Verifies service readiness and database connectivity (SELECT 1)."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as exc:
        logger.error(f"Readiness probe failed database check: {exc}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unhealthy", "database": "disconnected", "error": str(exc)}


# Include versioned API router (/api/v1)
app.include_router(api_v1_router, prefix=settings.API_PREFIX)
