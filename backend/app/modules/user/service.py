from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.user.repository import UserRepository
from app.modules.user.models import UserModel
from app.modules.user.schemas import (
    UserResponse,
    UserStatsResponse,
    UserProfileResponse,
    LearningSummaryResponse,
)
from app.modules.gamification.service import GamificationService
from app.modules.progress.service import ProgressService
from app.shared.errors import NotFoundError


class UserService:
    """Encapsulates business logic for the User domain and Profile BFF composition."""

    def __init__(self, repository: UserRepository, db: Optional[Session] = None):
        self.repository = repository
        self.db = db or repository.db

    def get_me(self, user: UserModel) -> UserResponse:
        return UserResponse.model_validate(user)

    def get_me_stats(self, user: UserModel) -> UserStatsResponse:
        if not user.stats:
            raise NotFoundError("User statistics not found for current user.")
        return UserStatsResponse.model_validate(user.stats)

    def get_user_profile(self, user: UserModel) -> UserProfileResponse:
        gamification_service = GamificationService(self.db)
        progress_service = ProgressService(self.db)

        user_resp = UserResponse.model_validate(user)
        stats_resp = gamification_service.get_user_stats(user)
        progress_summary = progress_service.get_user_progress_summary(user)

        total_skills = len(progress_summary.skills)
        skills_completed = sum(1 for s in progress_summary.skills if s.status == "completed")
        skills_in_progress = sum(1 for s in progress_summary.skills if s.status == "in_progress")
        total_lessons_completed = sum(s.lessons_completed for s in progress_summary.skills)

        course_progress_percent = (
            float(min(100.0, (skills_completed / max(1, total_skills)) * 100.0))
        )

        learning_summary = LearningSummaryResponse(
            lessons_completed=total_lessons_completed,
            skills_completed=skills_completed,
            skills_in_progress=skills_in_progress,
            course_progress_percent=round(course_progress_percent, 1),
        )

        return UserProfileResponse(
            user=user_resp,
            stats=stats_resp,
            learning=learning_summary,
        )
