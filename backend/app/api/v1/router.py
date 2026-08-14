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
from app.modules.home.router import router as home_router
from app.modules.social.router import router as social_router
from app.modules.search.router import router as search_router
from app.modules.vocabulary.router import router as vocabulary_router
from app.modules.quests.router import router as quest_router
from app.modules.notifications.router import router as notifications_router
from app.modules.ops.router import router as ops_router

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
api_v1_router.include_router(home_router)
api_v1_router.include_router(social_router)
api_v1_router.include_router(search_router)
api_v1_router.include_router(vocabulary_router)
api_v1_router.include_router(quest_router)
api_v1_router.include_router(notifications_router)
api_v1_router.include_router(ops_router)
