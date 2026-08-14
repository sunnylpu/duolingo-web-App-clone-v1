from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.modules.course.schemas import CourseSummaryResponse


class ContinueLearningSummary(BaseModel):
    unit_id: Optional[str] = None
    unit_title: Optional[str] = None
    skill_id: Optional[str] = None
    skill_title: Optional[str] = None
    lesson_id: Optional[str] = None
    lesson_title: Optional[str] = None
    progress_percent: float = 0.0
    lessons_completed: int = 0
    total_lessons: int = 0


class HomeDailyGoalSummary(BaseModel):
    xp: int = 0
    goal: int = 30
    goal_completed: bool = False
    goal_just_completed: bool = False


class HomeStreakSummary(BaseModel):
    current_streak: int = 0
    longest_streak: int = 0
    is_active_today: bool = False


class HomeHeartsSummary(BaseModel):
    hearts: int = 5
    max_hearts: int = 5
    next_heart_refill_seconds: Optional[int] = None


class HomeDashboardResponse(BaseModel):
    course: CourseSummaryResponse
    continue_learning: ContinueLearningSummary
    daily_goal: HomeDailyGoalSummary
    streak: HomeStreakSummary
    hearts: HomeHeartsSummary
    courses: List[CourseSummaryResponse] = []

    model_config = ConfigDict(from_attributes=True)
