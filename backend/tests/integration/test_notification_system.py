"""
Integration tests for Phase 31 — Notifications + Reminder System + Daily Engagement.

Verifies:
1. Notification model, user notification querying, and unread counts
2. Read state transitions (mark_as_read with ownership check, mark_all_as_read)
3. Notification preferences GET/PATCH API and preference enforcement
4. Automated reminder eligibility (daily, streak, quest)
5. Idempotent reminder generation with delivery deduplication ledger
"""

import pytest
import datetime
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel
from app.modules.user.repository import UserRepository
from app.modules.notifications.service import NotificationService
from app.modules.notifications.reminder_service import ReminderService
from app.modules.notifications.schemas import NotificationPreferenceUpdate
from app.shared.errors import NotFoundError
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_notification_creation_and_querying(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    notif_svc = NotificationService(seeded_db)

    # Create test notification
    n = notif_svc.create_notification(
        user_id=user_demo.id,
        notif_type="DAILY_REMINDER",
        title="Test Title",
        message="Test Message",
    )
    assert n is not None

    res = notif_svc.get_user_notifications(user_demo)
    assert res.total >= 1
    assert res.unread_count >= 1
    assert res.items[0].title == "Test Title"


def test_notification_read_ownership_enforcement(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    user_polyglot = seeded_db.query(UserModel).filter_by(id="usr_polyglot").first()
    notif_svc = NotificationService(seeded_db)

    n_demo = notif_svc.create_notification(
        user_id=user_demo.id,
        notif_type="ACHIEVEMENT_UNLOCKED",
        title="Demo Badge",
        message="Earned 100 XP",
    )

    # Polyglot trying to mark Demo's notification as read MUST raise NotFoundError
    with pytest.raises(NotFoundError):
        notif_svc.mark_as_read(user_polyglot, n_demo.id)

    # Demo marking own notification as read
    assert notif_svc.mark_as_read(user_demo, n_demo.id) is True
    res_after = notif_svc.get_user_notifications(user_demo, unread_only=True)
    assert not any(item.id == n_demo.id for item in res_after.items)


def test_notification_mark_all_read(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    notif_svc = NotificationService(seeded_db)

    notif_svc.create_notification(user_demo.id, "QUEST_REMINDER", "Q1", "Desc 1")
    notif_svc.create_notification(user_demo.id, "QUEST_REMINDER", "Q2", "Desc 2")

    count = notif_svc.mark_all_as_read(user_demo)
    assert count >= 2

    res = notif_svc.get_user_notifications(user_demo, unread_only=True)
    assert res.unread_count == 0


def test_notification_preferences_enforcement(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    notif_svc = NotificationService(seeded_db)

    # Disable achievement notifications
    notif_svc.update_preferences(
        user_demo, NotificationPreferenceUpdate(achievement_notifications=False)
    )

    # Create achievement notification
    res = notif_svc.create_notification(
        user_id=user_demo.id,
        notif_type="ACHIEVEMENT_UNLOCKED",
        title="Locked Title",
        message="Locked Message",
    )
    # Disabled preference returns None and suppresses creation
    assert res is None


def test_reminder_service_eligibility_and_deduplication(seeded_db: Session):
    user_repo = UserRepository(seeded_db)
    # Create user with streak but no daily activity for test_date
    test_user = user_repo.create_or_update_user(
        user_id="usr_test_reminders",
        username="test_reminders",
        display_name="Test Reminders",
        email="reminders@example.com",
    )

    reminder_svc = ReminderService(seeded_db)
    notif_svc = NotificationService(seeded_db)

    test_date = datetime.date(2026, 12, 1)

    # Initial reminder run
    count1 = reminder_svc.generate_all_reminders(test_date)
    assert count1 >= 1

    # Second run on same date must generate 0 due to delivery deduplication
    count2 = reminder_svc.generate_all_reminders(test_date)
    assert count2 == 0

    res = notif_svc.get_user_notifications(test_user)
    assert len(res.items) >= 1
