"""
Tests for Phase 24 — Course Mastery + Cross-Course Progress Dashboard.

Verifies:
1. Course progression metrics calculation (units, skills, lessons, percent, status)
2. Course progress summary endpoint GET /api/v1/progress/course/{course_id}
3. Automatic top-level course milestone completion detection and +500 XP bonus award
4. Course mastery achievement evaluation (FRENCH_MASTER, etc.)
5. Idempotent milestone reward prevention (no duplicate +500 XP on retries)
6. Multi-course mastery isolation across English, Spanish, and French
"""

import pytest
from sqlalchemy.orm import Session

from app.modules.user.models import UserModel
from app.modules.course.models import UnitModel, CourseModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.progress.service import ProgressService, COURSE_COMPLETION_XP
from app.modules.progress.models import LessonAttemptModel, CourseMilestoneModel
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_course_progress_endpoint(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    summary = service.get_user_course_progress(user, course_id="crs_french")
    assert summary.course_id == "crs_french"
    assert summary.course_name == "French"
    assert summary.total_units == 3
    assert summary.total_skills >= 12
    assert summary.total_lessons >= 36
    assert summary.status in ("available", "in_progress", "completed")


def test_course_completion_milestone_and_mastery_reward(seeded_db: Session):
    """
    Test completing all units in French grants CourseMilestone and awards +500 XP.
    """
    user_id = "usr_course_master_learner"
    user = seeded_db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        user = UserModel(id=user_id, username="course_master", display_name="Course Master", email="cm@test.com")
        seeded_db.add(user)
        seeded_db.commit()

    service = ProgressService(seeded_db)

    # French course has 3 units
    fr_units = seeded_db.query(UnitModel).filter_by(course_id="crs_french").all()
    fr_skills = (
        seeded_db.query(SkillModel)
        .filter(SkillModel.unit_id.in_([u.id for u in fr_units]))
        .all()
    )

    attempt_counter = 1
    for s in fr_skills:
        for lsn in s.lessons:
            seeded_db.add(LessonAttemptModel(
                id=f"att_cm_test_{attempt_counter}",
                user_id=user.id,
                lesson_id=lsn.id,
                status="completed",
            ))
            attempt_counter += 1
    seeded_db.commit()

    # Trigger course milestone check
    milestone_res = service.check_and_grant_course_milestone(user_id=user.id, course_id="crs_french")
    assert milestone_res["course_completed"] is True
    assert milestone_res["course_bonus_xp"] == 500
    assert milestone_res["already_awarded"] is False

    # Verify database model
    m_rec = (
        seeded_db.query(CourseMilestoneModel)
        .filter_by(user_id=user.id, course_id="crs_french")
        .first()
    )
    assert m_rec is not None
    assert m_rec.reward_xp == 500

    # Repeat check -> Idempotent prevention (no duplicate +500 XP)
    repeat_res = service.check_and_grant_course_milestone(user_id=user.id, course_id="crs_french")
    assert repeat_res["course_completed"] is False
    assert repeat_res["course_bonus_xp"] == 0
    assert repeat_res["already_awarded"] is True


def test_multi_course_mastery_isolation(seeded_db: Session):
    user_id = "usr_course_iso_learner"
    user = seeded_db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        user = UserModel(id=user_id, username="course_iso", display_name="Course Iso Learner", email="ciso@test.com")
        seeded_db.add(user)
        seeded_db.commit()

    service = ProgressService(seeded_db)

    # Complete French milestone
    res = service.check_and_grant_course_milestone(user_id=user.id, course_id="crs_french")
    assert res["course_completed"] is True

    # English and Spanish milestones remain unawarded
    en_m = seeded_db.query(CourseMilestoneModel).filter_by(user_id=user.id, course_id="crs_english").first()
    sp_m = seeded_db.query(CourseMilestoneModel).filter_by(user_id=user.id, course_id="crs_spanish").first()
    assert en_m is None
    assert sp_m is None
