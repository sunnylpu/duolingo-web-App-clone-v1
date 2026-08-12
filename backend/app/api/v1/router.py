from fastapi import APIRouter
from app.modules.user.router import router as user_router
from app.modules.course.router import router as course_router, path_router
from app.modules.lesson.router import router as lesson_router
from app.modules.progress.router import router as progress_router
from app.modules.gamification.router import (
    router as gamification_router,
    achievement_router,
)
from app.modules.leaderboard.router import router as leaderboard_router

api_v1_router = APIRouter()

# Register all domain routers under /api/v1
api_v1_router.include_router(user_router)
api_v1_router.include_router(course_router)
api_v1_router.include_router(path_router)
api_v1_router.include_router(lesson_router)
api_v1_router.include_router(progress_router)
api_v1_router.include_router(gamification_router)
api_v1_router.include_router(leaderboard_router)
api_v1_router.include_router(achievement_router)
