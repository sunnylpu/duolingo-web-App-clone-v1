from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, Field


class HeartRegenerationInfo(BaseModel):
    enabled: bool = True
    seconds_until_next: Optional[int] = None
    interval_seconds: int = 1800


class GamificationStatsResponse(BaseModel):
    total_xp: int
    current_streak: int
    longest_streak: int
    hearts: int
    max_hearts: int = 5
    heart_regeneration: Optional[HeartRegenerationInfo] = None
    gems: int
    daily_goal_xp: int
    daily_xp: int
    daily_goal_completed: bool = False
    activity_date: str = ""

    model_config = ConfigDict(from_attributes=True)


class DailyActivityResponse(BaseModel):
    date: str
    xp_earned: int
    lessons_completed: int
    goal_xp: int
    goal_completed: bool

    model_config = ConfigDict(from_attributes=True)


class AchievementResponse(BaseModel):
    id: str
    code: str
    name: str
    description: str
    icon: str
    requirement_type: str
    requirement_value: int

    model_config = ConfigDict(from_attributes=True)


class UserAchievementResponse(BaseModel):
    achievement: AchievementResponse
    is_earned: bool
    earned_at: Optional[datetime] = None
    progress: int = 0
    target: int = 1

    model_config = ConfigDict(from_attributes=True)


class PracticeExerciseResponse(BaseModel):
    exercise_id: str
    prompt: str
    type: str
    correct_answer: str
    data: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class PracticeSubmissionRequest(BaseModel):
    exercise_id: str
    answer: Union[str, Dict[str, Any], List[Any]]


class PracticeSubmissionResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    hearts: int
    max_hearts: int = 5
    recovered: int = 1

    model_config = ConfigDict(from_attributes=True)


class HeartRefillResponse(BaseModel):
    hearts: int
    max_hearts: int = 5
    refilled: bool = True

    model_config = ConfigDict(from_attributes=True)
