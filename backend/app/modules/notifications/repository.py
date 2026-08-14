import json
import datetime
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.modules.notifications.models import (
    NotificationModel,
    NotificationPreferenceModel,
    NotificationDeliveryModel,
)


class NotificationRepository:
    """Database persistence repository for notifications and preferences."""

    def __init__(self, db: Session):
        self.db = db

    def create_notification(
        self,
        notification_id: str,
        user_id: str,
        notif_type: str,
        title: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> NotificationModel:
        meta_str = json.dumps(metadata) if metadata else None
        notif = NotificationModel(
            id=notification_id,
            user_id=user_id,
            type=notif_type,
            title=title,
            message=message,
            metadata_json=meta_str,
            is_read=False,
        )
        self.db.add(notif)
        self.db.flush()
        return notif

    def get_user_notifications(
        self, user_id: str, unread_only: bool = False, limit: int = 20, offset: int = 0
    ) -> Tuple[List[NotificationModel], int, int]:
        query = self.db.query(NotificationModel).filter(NotificationModel.user_id == user_id)
        if unread_only:
            query = query.filter(NotificationModel.is_read == False)

        total = query.count()
        unread_count = (
            self.db.query(NotificationModel)
            .filter(NotificationModel.user_id == user_id, NotificationModel.is_read == False)
            .count()
        )

        items = (
            query.order_by(NotificationModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return items, unread_count, total

    def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        notif = (
            self.db.query(NotificationModel)
            .filter_by(id=notification_id, user_id=user_id)
            .first()
        )
        if notif:
            notif.is_read = True
            self.db.flush()
            return True
        return False

    def mark_all_as_read(self, user_id: str) -> int:
        count = (
            self.db.query(NotificationModel)
            .filter_by(user_id=user_id, is_read=False)
            .update({"is_read": True})
        )
        self.db.flush()
        return count

    def get_or_create_preferences(self, user_id: str) -> NotificationPreferenceModel:
        pref = self.db.query(NotificationPreferenceModel).filter_by(user_id=user_id).first()
        if not pref:
            pref = NotificationPreferenceModel(
                id=f"pref_{user_id}",
                user_id=user_id,
                daily_reminders=True,
                streak_reminders=True,
                quest_reminders=True,
                social_notifications=True,
                achievement_notifications=True,
            )
            self.db.add(pref)
            self.db.flush()
        return pref

    def update_preferences(
        self, user_id: str, updates: Dict[str, Any]
    ) -> NotificationPreferenceModel:
        pref = self.get_or_create_preferences(user_id)
        for key, val in updates.items():
            if val is not None and hasattr(pref, key):
                setattr(pref, key, val)
        self.db.flush()
        return pref

    def has_delivery_record(
        self, user_id: str, notif_type: str, ref_date: datetime.date
    ) -> bool:
        return (
            self.db.query(NotificationDeliveryModel)
            .filter_by(user_id=user_id, notification_type=notif_type, reference_date=ref_date)
            .first()
            is not None
        )

    def record_delivery(
        self, delivery_id: str, user_id: str, notif_type: str, ref_date: datetime.date
    ) -> NotificationDeliveryModel:
        delivery = NotificationDeliveryModel(
            id=delivery_id,
            user_id=user_id,
            notification_type=notif_type,
            reference_date=ref_date,
        )
        self.db.add(delivery)
        self.db.flush()
        return delivery
