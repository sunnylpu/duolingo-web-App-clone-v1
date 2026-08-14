from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class QuestItemResponse(BaseModel):
    id: str
    code: str
    title: str
    description: str
    quest_type: str
    quest_scope: str  # "daily", "weekly"
    current_value: int = 0
    target_value: int
    reward_xp: int
    completed: bool = False
    completed_at: Optional[datetime] = None
    course_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class DailyQuestsResponse(BaseModel):
    date: str
    user_id: str
    quests: List[QuestItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class WeeklyChallengeResponse(BaseModel):
    week_start_date: str
    challenge: Optional[QuestItemResponse] = None

    model_config = ConfigDict(from_attributes=True)


class QuestHistoryResponse(BaseModel):
    total_completed: int
    quests: List[QuestItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
