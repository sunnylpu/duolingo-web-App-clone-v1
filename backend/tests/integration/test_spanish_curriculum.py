"""
Tests for Phase 21 — Spanish Expansion & Course-Specific Progress Isolation.

Verifies:
1. Spanish course has 5 units, 20 skills, 60 lessons, 360 exercises
2. Preserved stable skill IDs (skill_greetings, skill_basics, skill_food, skill_family, skill_directions, skill_travel)
3. Every skill has objective and difficulty metadata (1 to 5)
4. Linear prerequisite chain across all 20 skills
5. All 6 exercise types represented with deterministic generation
6. Path API isolates content by course_id
7. Same learner can maintain independent progress in English and Spanish without cross-course interference
"""

import pytest
from sqlalchemy.orm import Session

from app.modules.user.models import UserModel
from app.modules.course.models import CourseModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.progress.service import ProgressService
from app.modules.progress.models import LessonAttemptModel, SkillProgressModel
from seed.generators.course_generator import generate_course
from seed.catalogs.spanish import SPANISH_COURSE_SPEC
from seed.seed import seed_database


@pytest.fixture(scope="module")
def spanish_catalog():
    return generate_course(SPANISH_COURSE_SPEC)


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


# ─────────────────────────────────────────────────────────────────────────────
# 1. Catalog Structure Verification Tests
# ─────────────────────────────────────────────────────────────────────────────

def test_spanish_course_metadata(spanish_catalog):
    assert spanish_catalog["id"] == "crs_spanish"
    assert spanish_catalog["name"] == "Spanish"
    assert spanish_catalog["code"] == "es"
    assert spanish_catalog["source_language"] == "en"
    assert spanish_catalog["target_language"] == "es"


def test_spanish_units_count(spanish_catalog):
    units = spanish_catalog["units"]
    assert len(units) == 5, f"Expected 5 units in Spanish course, found {len(units)}"


def test_spanish_skills_count(spanish_catalog):
    units = spanish_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    assert len(all_skills) == 20, f"Expected 20 skills in Spanish course, found {len(all_skills)}"


def test_spanish_lessons_count(spanish_catalog):
    units = spanish_catalog["units"]
    all_lessons = [lesson for unit in units for skill in unit["skills"] for lesson in skill["lessons"]]
    assert len(all_lessons) == 60, f"Expected 60 lessons in Spanish course, found {len(all_lessons)}"


def test_spanish_exercises_count(spanish_catalog):
    units = spanish_catalog["units"]
    all_exercises = [
        ex for unit in units for skill in unit["skills"] for lesson in skill["lessons"] for ex in lesson["exercises"]
    ]
    assert len(all_exercises) == 360, f"Expected 360 exercises in Spanish course, found {len(all_exercises)}"


def test_preserved_stable_skill_ids(spanish_catalog):
    units = spanish_catalog["units"]
    all_skill_ids = {skill["id"] for unit in units for skill in unit["skills"]}
    expected_stable_ids = {
        "skill_greetings",
        "skill_basics",
        "skill_food",
        "skill_family",
        "skill_directions",
        "skill_travel",
    }
    assert expected_stable_ids.issubset(all_skill_ids), (
        f"Missing preserved stable skill IDs: {expected_stable_ids - all_skill_ids}"
    )


def test_every_spanish_skill_has_objective_and_difficulty(spanish_catalog):
    units = spanish_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    for skill in all_skills:
        assert skill.get("objective"), f"Spanish skill '{skill['id']}' missing objective"
        assert 1 <= skill.get("difficulty", 0) <= 5, (
            f"Spanish skill '{skill['id']}' has invalid difficulty {skill.get('difficulty')}"
        )


def test_every_spanish_skill_has_three_lessons(spanish_catalog):
    units = spanish_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    for skill in all_skills:
        lessons = skill["lessons"]
        assert len(lessons) == 3, f"Spanish skill '{skill['id']}' expected 3 lessons, got {len(lessons)}"


def test_all_six_exercise_types_represented_in_spanish(spanish_catalog):
    units = spanish_catalog["units"]
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
    assert expected_types == types_found, f"Missing exercise types in Spanish catalog: {expected_types - types_found}"


def test_spanish_prerequisite_chain(spanish_catalog):
    units = spanish_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]

    assert all_skills[0]["prerequisite_skill_id"] is None
    for i in range(1, len(all_skills)):
        curr_skill = all_skills[i]
        prev_skill = all_skills[i - 1]
        assert curr_skill["prerequisite_skill_id"] == prev_skill["id"], (
            f"Skill '{curr_skill['id']}' prerequisite should be '{prev_skill['id']}', got '{curr_skill['prerequisite_skill_id']}'"
        )


# ─────────────────────────────────────────────────────────────────────────────
# 2. Course Path & Progress Isolation Tests
# ─────────────────────────────────────────────────────────────────────────────

def test_path_course_selection_isolation(seeded_db: Session):
    """Verify GET /path with course_id parameter returns isolated course content."""
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    # Spanish path
    sp_path = service.get_learning_path(user, course_id="crs_spanish")
    assert sp_path.course.id == "crs_spanish"
    sp_skill_ids = [s.id for u in sp_path.units for s in u.skills]
    assert len(sp_skill_ids) == 20
    assert "skill_greetings" in sp_skill_ids
    assert "skill_en_greetings" not in sp_skill_ids

    # English path
    en_path = service.get_learning_path(user, course_id="crs_english")
    assert en_path.course.id == "crs_english"
    en_skill_ids = [s.id for u in en_path.units for s in u.skills]
    assert len(en_skill_ids) == 32
    assert "skill_en_greetings" in en_skill_ids
    assert "skill_greetings" not in en_skill_ids

    # Default path (should default to flagship English course)
    default_path = service.get_learning_path(user)
    assert default_path.course.id == "crs_english"


def test_independent_user_progress_across_courses(seeded_db: Session):
    """
    Verify that the same learner maintains independent progress in English and Spanish.
    Completing a lesson in Spanish updates Spanish progress without modifying English progress.
    """
    user_id = "usr_polyglot_test"
    user = seeded_db.query(UserModel).filter_by(id=user_id).first()
    if not user:
        user = UserModel(id=user_id, username="polyglot_test", display_name="PolyGlot Test", email="polytest@test.com")
        seeded_db.add(user)
        seeded_db.commit()

    service = ProgressService(seeded_db)

    # Complete first lesson of Spanish Greetings (lsn_es_skill_greetings_1)
    sp_skill = seeded_db.query(SkillModel).filter_by(id="skill_greetings").first()
    assert sp_skill is not None
    sp_lesson = sp_skill.lessons[0]

    seeded_db.add(LessonAttemptModel(
        id="att_sp_poly_1",
        user_id=user.id,
        lesson_id=sp_lesson.id,
        status="completed",
    ))
    seeded_db.commit()

    # Fetch Spanish path & English path for this user
    sp_path = service.get_learning_path(user, course_id="crs_spanish")
    en_path = service.get_learning_path(user, course_id="crs_english")

    sp_greetings = [s for u in sp_path.units for s in u.skills if s.id == "skill_greetings"][0]
    en_greetings = [s for u in en_path.units for s in u.skills if s.id == "skill_en_greetings"][0]

    # Spanish greetings is in_progress
    assert sp_greetings.status == "in_progress"
    assert sp_greetings.completion_percent > 0

    # English greetings remains untouched (available / 0%)
    assert en_greetings.status == "available"
    assert en_greetings.completion_percent == 0.0

    # Now complete first lesson of English Greetings
    en_skill = seeded_db.query(SkillModel).filter_by(id="skill_en_greetings").first()
    assert en_skill is not None
    en_lesson = en_skill.lessons[0]

    seeded_db.add(LessonAttemptModel(
        id="att_en_poly_1",
        user_id=user.id,
        lesson_id=en_lesson.id,
        status="completed",
    ))
    seeded_db.commit()

    # Re-fetch paths
    sp_path2 = service.get_learning_path(user, course_id="crs_spanish")
    en_path2 = service.get_learning_path(user, course_id="crs_english")

    sp_greetings2 = [s for u in sp_path2.units for s in u.skills if s.id == "skill_greetings"][0]
    en_greetings2 = [s for u in en_path2.units for s in u.skills if s.id == "skill_en_greetings"][0]

    # Both courses now independently track progress for the same user
    assert sp_greetings2.status == "in_progress"
    assert en_greetings2.status == "in_progress"
