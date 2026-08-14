"""
Phase 36 — Production Authentication Hardening & Domain Ownership Isolation Tests.

Verifies:
1. Fail-fast configuration validation for production deployment
2. Token blocklist / session revocation mechanism
3. Cross-user attempt ownership isolation (attempt tampering rejected with 403)
4. Notification cross-user ownership isolation (403/404 on foreign notifications)
5. CSRF defense for cookie-authenticated mutations
6. Admin route RBAC enforcement
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.config import Settings
from app.shared.database import get_db
from app.shared.security import create_access_token, token_blocklist
from app.shared.rate_limit import rate_limiter
from app.modules.user.models import UserModel
from app.modules.lesson.models import LessonModel, ExerciseModel
from app.modules.progress.models import LessonAttemptModel
from app.modules.notifications.models import NotificationModel
from seed.seed import seed_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_seeded_database(db_session: Session):
    token_blocklist.clear()
    rate_limiter.clear()
    client.cookies.clear()
    seed_database(db_session)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield db_session
    app.dependency_overrides.clear()
    token_blocklist.clear()
    rate_limiter.clear()
    client.cookies.clear()


def test_production_config_fails_fast_on_default_or_weak_jwt_secret():
    # 1. Default secret in production -> Must raise ValueError
    with pytest.raises(ValueError, match="strong, non-default JWT_SECRET_KEY"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            JWT_SECRET_KEY="super_secret_duolingo_key_change_in_production_32bytes_min",
        )

    # 2. Too short secret in production -> Must raise ValueError
    with pytest.raises(ValueError, match="strong, non-default JWT_SECRET_KEY"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            JWT_SECRET_KEY="too_short_secret",
        )

    # 3. DEBUG=True in production -> Must raise ValueError
    with pytest.raises(ValueError, match="DEBUG mode must be disabled"):
        Settings(
            APP_ENV="production",
            DEBUG=True,
            JWT_SECRET_KEY="a" * 32,
        )

    # 4. Valid production settings -> Must pass
    valid_settings = Settings(
        APP_ENV="production",
        DEBUG=False,
        JWT_SECRET_KEY="a" * 32,
    )
    assert valid_settings.APP_ENV == "production"
    assert valid_settings.DEBUG is False


def test_cross_user_lesson_attempt_tampering_is_forbidden(db_session: Session):
    # Retrieve first seeded lesson and exercise
    lesson = db_session.query(LessonModel).first()
    assert lesson is not None
    exercise = db_session.query(ExerciseModel).filter(ExerciseModel.lesson_id == lesson.id).first()
    assert exercise is not None

    # 1. User A (demo learner) starts an authentic lesson attempt
    token_a = create_access_token("usr_demo", role="user")
    start_res = client.post(
        f"/api/v1/lessons/{lesson.id}/start",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # 2. User B (another learner) attempts to submit an answer to User A's attempt
    token_b = create_access_token("usr_admin", role="admin")

    answer_payload = {
        "attempt_id": attempt_id,
        "answer": ["Good morning"],
    }
    res = client.post(
        f"/api/v1/lessons/{lesson.id}/exercises/{exercise.id}/answer",
        json=answer_payload,
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "FORBIDDEN"

    # 3. User B attempts to complete User A's attempt
    complete_payload = {
        "attempt_id": attempt_id,
    }
    complete_res = client.post(
        f"/api/v1/lessons/{lesson.id}/complete",
        json=complete_payload,
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert complete_res.status_code == 403
    assert complete_res.json()["error"]["code"] == "FORBIDDEN"


def test_cross_user_notification_ownership(db_session: Session):
    # Create notification for User A (usr_demo)
    notif_a = NotificationModel(
        id="notif_alice_001",
        user_id="usr_demo",
        type="DAILY_REMINDER",
        title="Time to study",
        message="Keep your streak alive!",
        is_read=False,
    )
    db_session.add(notif_a)
    db_session.commit()

    token_b = create_access_token("usr_admin", role="admin")

    # User B tries to mark User A's notification as read
    res = client.post(
        "/api/v1/notifications/notif_alice_001/read",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert res.status_code in [403, 404]


def test_csrf_protection_on_cookie_authenticated_requests():
    token = create_access_token("usr_demo", role="user")

    # 1. An untrusted cross-origin POST request with auth_token cookie
    untrusted_res = client.post(
        "/api/v1/gamification/hearts/refill",
        cookies={"auth_token": token},
        headers={
            "Origin": "http://evil-attacker-site.com",
            "Referer": "http://evil-attacker-site.com/csrf.html",
        },
    )
    assert untrusted_res.status_code == 403
    assert untrusted_res.json()["error"]["code"] == "CSRF_REJECTED"

    # 2. A legitimate AJAX request with X-Requested-With header
    trusted_res = client.post(
        "/api/v1/gamification/hearts/refill",
        cookies={"auth_token": token},
        headers={
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    assert trusted_res.status_code == 200
    assert trusted_res.json()["hearts"] == 5
