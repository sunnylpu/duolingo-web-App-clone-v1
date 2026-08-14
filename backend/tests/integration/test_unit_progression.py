"""
Tests for Phase 23 — Unit Progression + Mastery + Milestone Rewards.

Verifies:
1. Unit progression metrics calculation (completed_skills, total_skills, completion_percent)
2. Unit statuses (locked, available, in_progress, completed)
3. Unit progress endpoint GET /api/v1/progress/units
4. Automatic unit milestone completion detection and +50 XP bonus award
5. Idempotent milestone reward prevention (no duplicate +50 XP on retries)
6. Multi-course unit progress isolation across English, Spanish, and French
"""

import pytest
from sqlalchemy.orm import Session

from app.modules.user.models import UserModel
from app.modules.course.models import UnitModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.progress.service import ProgressService, UNIT_COMPLETION_XP
from app.modules.lesson.service import LessonService
from app.modules.progress.models import LessonAttemptModel, UnitMilestoneModel
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_unit_progression_metrics_in_path(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    path = service.get_learning_path(user, course_id="crs_english")
    assert len(path.units) == 8

    unit1 = path.units[0]
    assert unit1.total_skills == 4
    assert unit1.status in ("available", "in_progress", "completed")
    assert unit1.completion_percent >= 0.0


def test_get_user_unit_progress_endpoint_logic(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    units_summary = service.get_user_unit_progress(user, course_id="crs_english")
    assert len(units_summary) == 8
    for u in units_summary:
        assert u.total_skills > 0
        assert u.status in ("locked", "available", "in_progress", "completed")


def test_unit_completion_milestone_and_bonus_xp(seeded_db: Session):
    """
    Test that completing all skills in a unit automatically grants UnitMilestone and awards +50 XP.
    """
    user_id = "usr_unit_test_learner"
    user = seeded_db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        user = UserModel(id=user_id, username="unit_test", display_name="Unit Learner", email="unit@test.com")
        seeded_db.add(user)
        seeded_db.commit()

    service = ProgressService(seeded_db)

    # Unit 1 of French (unit_fr_01) has 4 skills: skill_fr_greetings, skill_fr_introductions, skill_fr_pronouns, skill_fr_verbs
    unit_fr_1 = seeded_db.query(UnitModel).filter_by(id="unit_fr_01").first()
    assert unit_fr_1 is not None

    skills = seeded_db.query(SkillModel).filter_by(unit_id="unit_fr_01").all()
    assert len(skills) == 4

    # Mark all lessons of all 4 skills in unit_fr_01 as completed
    attempt_counter = 1
    for s in skills:
        for lsn in s.lessons:
            seeded_db.add(LessonAttemptModel(
                id=f"att_unit_fr_test_{attempt_counter}",
                user_id=user.id,
                lesson_id=lsn.id,
                status="completed",
            ))
            attempt_counter += 1
    seeded_db.commit()

    # Trigger milestone check
    milestone_res = service.check_and_grant_unit_milestone(user_id=user.id, unit_id="unit_fr_01")
    assert milestone_res["unit_completed"] is True
    assert milestone_res["unit_bonus_xp"] == 50
    assert milestone_res["already_awarded"] is False

    # Check database model record
    milestone_record = (
        seeded_db.query(UnitMilestoneModel)
        .filter_by(user_id=user.id, unit_id="unit_fr_01")
        .first()
    )
    assert milestone_record is not None
    assert milestone_record.reward_xp == 50

    # Repeat milestone check -> Idempotent prevention (no duplicate +50 XP)
    repeat_res = service.check_and_grant_unit_milestone(user_id=user.id, unit_id="unit_fr_01")
    assert repeat_res["unit_completed"] is False
    assert repeat_res["unit_bonus_xp"] == 0
    assert repeat_res["already_awarded"] is True


def test_multi_course_unit_progress_isolation(seeded_db: Session):
    user_id = "usr_unit_iso_learner"
    user = seeded_db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        user = UserModel(id=user_id, username="unit_iso", display_name="Unit Iso Learner", email="iso@test.com")
        seeded_db.add(user)
        seeded_db.commit()

    service = ProgressService(seeded_db)

    # Complete unit milestone for Spanish unit 1 (unit_sp_01)
    milestone_res = service.check_and_grant_unit_milestone(user_id=user.id, unit_id="unit_sp_01")
    assert milestone_res["unit_completed"] is True

    # English unit 1 and French unit 1 milestones remain unawarded
    en_m = seeded_db.query(UnitMilestoneModel).filter_by(user_id=user.id, unit_id="unit_en_01").first()
    fr_m = seeded_db.query(UnitMilestoneModel).filter_by(user_id=user.id, unit_id="unit_fr_01").first()
    assert en_m is None
    assert fr_m is None
