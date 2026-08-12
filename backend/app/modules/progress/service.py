from app.modules.progress.repository import ProgressRepository
from app.modules.progress.schemas import ProgressResponse, SkillProgressSummary
from app.modules.user.models import UserModel


class ProgressService:
    """Contains business logic for Progress domain."""

    def __init__(self, repository: ProgressRepository):
        self.repository = repository

    def get_user_progress_summary(self, current_user: UserModel) -> ProgressResponse:
        records = self.repository.get_user_skill_progresses(current_user.id)
        summaries = [
            SkillProgressSummary(
                skill_id=r.skill_id,
                status=r.status,
                completion_percent=r.completion_percent,
                crown_level=r.crown_level,
                lessons_completed=r.lessons_completed,
                xp_earned=r.xp_earned,
            )
            for r in records
        ]
        return ProgressResponse(skills=summaries)
