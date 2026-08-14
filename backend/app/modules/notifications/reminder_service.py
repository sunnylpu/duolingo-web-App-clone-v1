import uuid
import datetime
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel
from app.modules.gamification.models import UserStatsModel
from app.modules.progress.models import DailyActivityModel
from app.modules.quests.models import UserQuestModel
from app.modules.notifications.repository import NotificationRepository
from app.modules.notifications.service import NotificationService
from app.modules.gamification.service import get_current_activity_date


class ReminderService:
    """Evaluates candidate eligibility and issues automated daily/streak/quest reminders."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = NotificationRepository(db)
        self.notification_service = NotificationService(db)

    def get_daily_reminder_candidates(self, ref_date: datetime.date) -> List[UserModel]:
        # Users without DailyActivity for ref_date & daily_reminders enabled
        active_today_user_ids = {
            act.user_id
            for act in self.db.query(DailyActivityModel.user_id)
            .filter(DailyActivityModel.activity_date == ref_date)
            .all()
        }

        all_users = self.db.query(UserModel).all()
        candidates: List[UserModel] = []
        for u in all_users:
            if u.id in active_today_user_ids:
                continue
            pref = self.repository.get_or_create_preferences(u.id)
            if pref.daily_reminders:
                candidates.append(u)
        return candidates

    def get_streak_reminder_candidates(self, ref_date: datetime.date) -> List[Tuple[UserModel, int]]:
        active_today_user_ids = {
            act.user_id
            for act in self.db.query(DailyActivityModel.user_id)
            .filter(DailyActivityModel.activity_date == ref_date)
            .all()
        }

        candidates: List[Tuple[UserModel, int]] = []
        stats_list = self.db.query(UserStatsModel).filter(UserStatsModel.current_streak > 0).all()
        for st in stats_list:
            if st.user_id in active_today_user_ids:
                continue
            u = self.db.query(UserModel).filter_by(id=st.user_id).first()
            if not u:
                continue
            pref = self.repository.get_or_create_preferences(u.id)
            if pref.streak_reminders:
                candidates.append((u, st.current_streak))
        return candidates

    def generate_all_reminders(self, ref_date: Optional[datetime.date] = None) -> int:
        today = ref_date or get_current_activity_date()
        generated_count = 0

        # 1. Generate Streak Reminders
        streak_candidates = self.get_streak_reminder_candidates(today)
        for user, streak_val in streak_candidates:
            notif_type = "STREAK_REMINDER"
            if not self.repository.has_delivery_record(user.id, notif_type, today):
                self.notification_service.create_notification(
                    user_id=user.id,
                    notif_type=notif_type,
                    title="🔥 Streak Alert!",
                    message=f"Keep your {streak_val}-day streak alive! Complete a lesson before midnight.",
                    metadata={"streak": streak_val},
                )
                self.repository.record_delivery(
                    delivery_id=f"del_{uuid.uuid4().hex[:12]}",
                    user_id=user.id,
                    notif_type=notif_type,
                    ref_date=today,
                )
                generated_count += 1

        # 2. Generate Daily Reminders
        daily_candidates = self.get_daily_reminder_candidates(today)
        for user in daily_candidates:
            notif_type = "DAILY_REMINDER"
            if not self.repository.has_delivery_record(user.id, notif_type, today):
                self.notification_service.create_notification(
                    user_id=user.id,
                    notif_type=notif_type,
                    title="🔔 Time to Practice!",
                    message="Spend 5 minutes today to practice your language skills.",
                )
                self.repository.record_delivery(
                    delivery_id=f"del_{uuid.uuid4().hex[:12]}",
                    user_id=user.id,
                    notif_type=notif_type,
                    ref_date=today,
                )
                generated_count += 1

        self.db.commit()
        return generated_count
