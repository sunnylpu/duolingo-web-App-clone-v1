from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.shared.database import init_db
from app.shared.logging import setup_logging
from app.shared.middleware import setup_middleware
from app.shared.errors import setup_exception_handlers

# Import domain routers
from app.modules.user.router import router as user_router
from app.modules.course.router import router as course_router
from app.modules.lesson.router import router as lesson_router
from app.modules.progress.router import router as progress_router
from app.modules.gamification.router import router as gamification_router
from app.modules.leaderboard.router import router as leaderboard_router

logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events lifecycle manager."""
    logger.info(f"Starting {settings.APP_NAME} service...")
    # Initialize database tables for development
    init_db()
    logger.info("Database schemas initialized.")
    yield
    logger.info(f"Shutting down {settings.APP_NAME} service...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Scalable full-stack Duolingo-style language learning API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup middleware & exception handlers
setup_middleware(app)
setup_exception_handlers(app)


# Root health check endpoint
@app.get("/health", tags=["system"])
def health_check():
    """
    Health check endpoint returning application status.
    Exposed at root /health for load balancer and readiness checks.
    """
    return {"status": "ok"}


# Include domain routers under API_PREFIX (/api/v1)
api_v1_prefix = settings.API_PREFIX
app.include_router(user_router, prefix=api_v1_prefix)
app.include_router(course_router, prefix=api_v1_prefix)
app.include_router(lesson_router, prefix=api_v1_prefix)
app.include_router(progress_router, prefix=api_v1_prefix)
app.include_router(gamification_router, prefix=api_v1_prefix)
app.include_router(leaderboard_router, prefix=api_v1_prefix)
