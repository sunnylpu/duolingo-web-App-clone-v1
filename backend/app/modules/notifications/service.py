import json
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.modules.notifications.repository import NotificationRepository
from app.modules.user.models import UserModel
from app.modules.notifications.schemas import (
    NotificationResponse,
    NotificationListResponse,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
)
from app.shared.errors import NotFoundError, ValidationError

PREFERENCE_MAPPING = {
    "DAILY_REMINDER": "daily_reminders",
    "STREAK_REMINDER": "streak_reminders",
    "QUEST_REMINDER": "quest_reminders",
    "ACHIEVEMENT_UNLOCKED": "achievement_notifications",
    "UNIT_COMPLETED": "achievement_notifications",
    "COURSE_COMPLETED": "achievement_notifications",
    "SOCIAL_ACTIVITY": "social_notifications",
}


class NotificationService:
    """Business logic for user notifications, read states, and delivery preferences."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = NotificationRepository(db)

    def get_user_notifications(
        self, current_user: UserModel, unread_only: bool = False, limit: int = 20, offset: int = 0
    ) -> NotificationListResponse:
        items, unread_count, total = self.repository.get_user_notifications(
            user_id=current_user.id, unread_only=unread_only, limit=limit, offset=offset
        )

        responses: List[NotificationResponse] = []
        for it in items:
            meta = json.loads(it.metadata_json) if it.metadata_json else None
            responses.append(
                NotificationResponse(
                    id=it.id,
                    user_id=it.user_id,
                    type=it.type,
                    title=it.title,
                    message=it.message,
                    metadata=meta,
                    is_read=it.is_read,
                    created_at=it.created_at,
                )
            )

        return NotificationListResponse(items=responses, unread_count=unread_count, total=total)

    def mark_as_read(self, current_user: UserModel, notification_id: str) -> bool:
        success = self.repository.mark_as_read(notification_id=notification_id, user_id=current_user.id)
        if not success:
            raise NotFoundError(f"Notification '{notification_id}' not found or belongs to another user.")
        self.db.commit()
        return True

    def mark_all_as_read(self, current_user: UserModel) -> int:
        count = self.repository.mark_all_as_read(user_id=current_user.id)
        self.db.commit()
        return count

    def get_preferences(self, current_user: UserModel) -> NotificationPreferenceResponse:
        pref = self.repository.get_or_create_preferences(current_user.id)
        self.db.commit()
        return NotificationPreferenceResponse.model_validate(pref)

    def update_preferences(
        self, current_user: UserModel, payload: NotificationPreferenceUpdate
    ) -> NotificationPreferenceResponse:
        updates = payload.model_dump(exclude_unset=True)
        pref = self.repository.update_preferences(current_user.id, updates)
        self.db.commit()
        return NotificationPreferenceResponse.model_validate(pref)

    def create_notification(
        self,
        user_id: str,
        notif_type: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[NotificationResponse]:
        # Respect user notification preferences
        pref = self.repository.get_or_create_preferences(user_id)
        pref_attr = PREFERENCE_MAPPING.get(notif_type)
        if pref_attr and getattr(pref, pref_attr, True) is False:
            return None  # Delivery disabled by learner preference

        notif_id = f"notif_{uuid.uuid4().hex[:12]}"
        notif = self.repository.create_notification(
            notification_id=notif_id,
            user_id=user_id,
            notif_type=notif_type,
            title=title,
            message=message,
            metadata=metadata,
        )
        self.db.commit()

        meta = json.loads(notif.metadata_json) if notif.metadata_json else None
        return NotificationResponse(
            id=notif.id,
            user_id=notif.user_id,
            type=notif.type,
            title=notif.title,
            message=notif.message,
            metadata=meta,
            is_read=notif.is_read,
            created_at=notif.created_at,
        )
