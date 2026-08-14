"""
Integration tests for Phase 23 — Unit Progression, Mastery & Milestone Rewards.

Verifies:
1. Unit progression metrics calculation within path response
2. Direct unit progress queries via API service
3. Unit milestone grants and XP rewards
4. Multi-course unit progress isolation
"""

import pytest
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel
from app.modules.course.models import UnitModel
from app.modules.progress.models import UnitMilestoneModel
from app.modules.progress.service import ProgressService
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_unit_progression_metrics_in_path(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)
    path = service.get_learning_path(user, course_id="crs_english")

    assert len(path.units) > 0
    unit1 = path.units[0]
    assert hasattr(unit1, "completion_percent") or hasattr(unit1, "completed_skills")
    assert unit1.total_skills == 4


def test_get_user_unit_progress_endpoint_logic(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)
    units_progress = service.get_user_unit_progress(user, course_id="crs_english")

    assert len(units_progress) > 0
    first_unit = units_progress[0]
    assert first_unit.unit_id == "unit_en_01"
    assert first_unit.total_skills == 4
    assert first_unit.completed_skills >= 0
    assert 0 <= first_unit.completion_percent <= 100


def test_unit_completion_milestone_and_bonus_xp(seeded_db: Session):
    user_id = "usr_demo"
    unit_id = "unit_en_01"

    service = ProgressService(seeded_db)

    # Grant unit milestone
    res = service.check_and_grant_unit_milestone(user_id=user_id, unit_id=unit_id)

    assert "unit_bonus_xp" in res
    assert res["unit_bonus_xp"] == 50

    milestone_after = (
        seeded_db.query(UnitMilestoneModel)
        .filter_by(user_id=user_id, unit_id=unit_id)
        .first()
    )
    assert milestone_after is not None

    # Duplicate grant attempt should be idempotent
    res_dup = service.check_and_grant_unit_milestone(user_id=user_id, unit_id=unit_id)
    assert res_dup.get("already_claimed") is True or res_dup.get("already_awarded") is True


def test_multi_course_unit_progress_isolation(seeded_db: Session):
    user_id = "usr_unit_iso_learner"
    user = seeded_db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        user = UserModel(id=user_id, username="unit_iso", display_name="Unit Iso Learner", email="iso@test.com")
        seeded_db.add(user)
        seeded_db.commit()

    service = ProgressService(seeded_db)

    # Complete unit milestone for Spanish unit 1 (unit_01)
    milestone_res = service.check_and_grant_unit_milestone(user_id=user.id, unit_id="unit_01")
    assert milestone_res["unit_completed"] is True

    # English unit 1 and French unit 1 milestones remain unawarded
    en_m = seeded_db.query(UnitMilestoneModel).filter_by(user_id=user.id, unit_id="unit_en_01").first()
    fr_m = seeded_db.query(UnitMilestoneModel).filter_by(user_id=user.id, unit_id="unit_fr_01").first()
    assert en_m is None
    assert fr_m is None
