from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    type: str
    title: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    is_read: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationListResponse(BaseModel):
    items: List[NotificationResponse] = []
    unread_count: int = 0
    total: int = 0

    model_config = ConfigDict(from_attributes=True)


class NotificationPreferenceResponse(BaseModel):
    user_id: str
    daily_reminders: bool = True
    streak_reminders: bool = True
    quest_reminders: bool = True
    social_notifications: bool = True
    achievement_notifications: bool = True

    model_config = ConfigDict(from_attributes=True)


class NotificationPreferenceUpdate(BaseModel):
    daily_reminders: Optional[bool] = None
    streak_reminders: Optional[bool] = None
    quest_reminders: Optional[bool] = None
    social_notifications: Optional[bool] = None
    achievement_notifications: Optional[bool] = None
