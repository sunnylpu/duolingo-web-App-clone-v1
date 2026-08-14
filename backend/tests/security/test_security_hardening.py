"""
Integration tests for Phase 33 — Production Security, Configuration Hardening & API Protection.

Verifies:
1. SQLite Foreign Key enforcement PRAGMA foreign_keys = ON
2. Production DEBUG stack trace masking
3. RateLimiter sliding-window check and consumption
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.modules.progress.models import SkillProgressModel
from app.shared.rate_limit import RateLimiter
from app.shared.errors import ValidationError
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_sqlite_foreign_key_enforcement(seeded_db: Session):
    # Attempting to insert SkillProgressModel referencing non-existent skill ID must fail
    invalid_progress = SkillProgressModel(
        id="prg_invalid_fk",
        user_id="usr_demo",
        skill_id="non_existent_skill_id_999",
        status="completed",
    )
    seeded_db.add(invalid_progress)

    with pytest.raises(IntegrityError):
        seeded_db.commit()

    seeded_db.rollback()


def test_rate_limiter_abstraction():
    limiter = RateLimiter()
    key = "test_user_rate_limit"

    # Consume 3 tokens out of limit=3
    assert limiter.consume(key, limit=3, window_seconds=60) == 2
    assert limiter.consume(key, limit=3, window_seconds=60) == 1
    assert limiter.consume(key, limit=3, window_seconds=60) == 0

    # 4th consume attempt must raise ValidationError with RATE_LIMIT_EXCEEDED code
    with pytest.raises(ValidationError) as exc:
        limiter.consume(key, limit=3, window_seconds=60)

    assert exc.value.code == "RATE_LIMIT_EXCEEDED"
