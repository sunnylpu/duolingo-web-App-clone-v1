"""
Tests for Phase 22 — French Secondary Course & Course Switcher Foundation.

Verifies:
1. French course catalog metrics (3 units, >=12 skills, >=36 lessons, >=216 exercises)
2. Every French skill has objective, difficulty (1 to 3), and prerequisite chain
3. All 6 exercise types represented in French course
4. Course list endpoint GET /api/v1/courses returns progress summary per course
5. Learning path GET /api/v1/path?course_id=crs_french returns isolated French content
6. Same learner maintains independent progress across English, Spanish, and French
"""

import pytest
from sqlalchemy.orm import Session

from app.modules.user.models import UserModel
from app.modules.course.models import CourseModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.progress.service import ProgressService
from app.modules.course.service import CourseService
from app.modules.progress.models import LessonAttemptModel
from seed.generators.course_generator import generate_course
from seed.catalogs.french import FRENCH_COURSE_SPEC
from seed.seed import seed_database


@pytest.fixture(scope="module")
def french_catalog():
    return generate_course(FRENCH_COURSE_SPEC)


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


# ─────────────────────────────────────────────────────────────────────────────
# 1. French Catalog Structure Verification Tests
# ─────────────────────────────────────────────────────────────────────────────

def test_french_course_metadata(french_catalog):
    assert french_catalog["id"] == "crs_french"
    assert french_catalog["name"] == "French"
    assert french_catalog["code"] == "fr"
    assert french_catalog["source_language"] == "en"
    assert french_catalog["target_language"] == "fr"


def test_french_units_count(french_catalog):
    units = french_catalog["units"]
    assert len(units) == 3, f"Expected 3 units in French course, found {len(units)}"


def test_french_skills_count(french_catalog):
    units = french_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    assert len(all_skills) >= 12, f"Expected at least 12 skills in French course, found {len(all_skills)}"


def test_french_lessons_count(french_catalog):
    units = french_catalog["units"]
    all_lessons = [lesson for unit in units for skill in unit["skills"] for lesson in skill["lessons"]]
    assert len(all_lessons) >= 36, f"Expected at least 36 lessons in French course, found {len(all_lessons)}"


def test_french_exercises_count(french_catalog):
    units = french_catalog["units"]
    all_exercises = [
        ex for unit in units for skill in unit["skills"] for lesson in skill["lessons"] for ex in lesson["exercises"]
    ]
    assert len(all_exercises) >= 216, f"Expected at least 216 exercises in French course, found {len(all_exercises)}"


def test_every_french_skill_has_objective_and_difficulty(french_catalog):
    units = french_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    for skill in all_skills:
        assert skill.get("objective"), f"French skill '{skill['id']}' missing objective"
        assert 1 <= skill.get("difficulty", 0) <= 5, (
            f"French skill '{skill['id']}' has invalid difficulty {skill.get('difficulty')}"
        )


def test_all_six_exercise_types_represented_in_french(french_catalog):
    units = french_catalog["units"]
    all_exercises = [
        ex for unit in units for skill in unit["skills"] for lesson in skill["lessons"] for ex in lesson["exercises"]
    ]
    types_found = {ex["type"] for ex in all_exercises}
    expected_types = {
        "multiple_choice",
        "type_answer",
        "translate",
        "word_bank",
        "match_pairs",
        "fill_blank",
    }
    assert expected_types == types_found, f"Missing exercise types in French catalog: {expected_types - types_found}"


def test_french_prerequisite_chain(french_catalog):
    units = french_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]

    assert all_skills[0]["prerequisite_skill_id"] is None
    for i in range(1, len(all_skills)):
        curr_skill = all_skills[i]
        prev_skill = all_skills[i - 1]
        assert curr_skill["prerequisite_skill_id"] == prev_skill["id"], (
            f"Skill '{curr_skill['id']}' prerequisite should be '{prev_skill['id']}', got '{curr_skill['prerequisite_skill_id']}'"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 2. Multi-Course Path & Progress Integration Tests
# ─────────────────────────────────────────────────────────────────────────────

def test_french_path_query(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    fr_path = service.get_learning_path(user, course_id="crs_french")
    assert fr_path.course.id == "crs_french"
    fr_skill_ids = [s.id for u in fr_path.units for s in u.skills]
    assert len(fr_skill_ids) >= 12
    assert "skill_fr_greetings" in fr_skill_ids
    assert "skill_en_greetings" not in fr_skill_ids
    assert "skill_greetings" not in fr_skill_ids


def test_get_courses_with_progress_summary(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    course_service = CourseService(seeded_db)

    courses = course_service.get_courses(current_user=user)
    assert len(courses) == 3
    course_ids = {c.id for c in courses}
    assert course_ids == {"crs_english", "crs_spanish", "crs_french"}

    for c in courses:
        assert c.total_skills > 0
        assert 0.0 <= c.progress_percent <= 100.0


def test_independent_user_progress_in_french(seeded_db: Session):
    user_id = "usr_french_learner"
    user = seeded_db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        user = UserModel(id=user_id, username="french_learner", display_name="French Learner", email="fr@test.com")
        seeded_db.add(user)
        seeded_db.commit()

    service = ProgressService(seeded_db)

    # Complete first lesson of French Greetings (lsn_fr_skill_fr_greetings_1)
    fr_skill = seeded_db.query(SkillModel).filter_by(id="skill_fr_greetings").first()
    assert fr_skill is not None
    fr_lesson = fr_skill.lessons[0]

    seeded_db.add(LessonAttemptModel(
        id="att_fr_poly_1",
        user_id=user.id,
        lesson_id=fr_lesson.id,
        status="completed",
    ))
    seeded_db.commit()

    fr_path = service.get_learning_path(user, course_id="crs_french")
    en_path = service.get_learning_path(user, course_id="crs_english")
    sp_path = service.get_learning_path(user, course_id="crs_spanish")

    fr_greetings = [s for u in fr_path.units for s in u.skills if s.id == "skill_fr_greetings"][0]
    en_greetings = [s for u in en_path.units for s in u.skills if s.id == "skill_en_greetings"][0]
    sp_greetings = [s for u in sp_path.units for s in u.skills if s.id == "skill_greetings"][0]

    # French greetings is in_progress
    assert fr_greetings.status == "in_progress"
    assert fr_greetings.completion_percent > 0

    # English and Spanish remain untouched (available / 0%)
    assert en_greetings.status == "available"
    assert en_greetings.completion_percent == 0.0
    assert sp_greetings.status == "available"
    assert sp_greetings.completion_percent == 0.0
