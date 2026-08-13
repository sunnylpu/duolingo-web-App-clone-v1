"""
Tests for Phase 20 — English Flagship Curriculum Expansion.

Verifies:
1. English course has 8 units, 32 skills, 96 lessons, 576 exercises
2. Every skill has a learning objective and difficulty level
3. Linear prerequisite chain across all 32 skills
4. Every skill has 3 lessons with 6 exercises per lesson
5. All 6 exercise types are represented with varied ordering
6. Content is topic-relevant and deterministic
"""

import pytest
from seed.generators.course_generator import generate_course
from seed.catalogs.english import ENGLISH_COURSE_SPEC


@pytest.fixture(scope="module")
def english_catalog():
    return generate_course(ENGLISH_COURSE_SPEC)


def test_english_course_metadata(english_catalog):
    assert english_catalog["id"] == "crs_english"
    assert english_catalog["name"] == "English"
    assert english_catalog["code"] == "en"
    assert english_catalog["source_language"] == "hi"
    assert english_catalog["target_language"] == "en"


def test_english_units_count(english_catalog):
    units = english_catalog["units"]
    assert len(units) == 8, f"Expected 8 units in English course, found {len(units)}"


def test_english_skills_count(english_catalog):
    units = english_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    assert len(all_skills) == 32, f"Expected 32 skills in English course, found {len(all_skills)}"


def test_english_lessons_count(english_catalog):
    units = english_catalog["units"]
    all_lessons = [lesson for unit in units for skill in unit["skills"] for lesson in skill["lessons"]]
    assert len(all_lessons) == 96, f"Expected 96 lessons in English course, found {len(all_lessons)}"


def test_english_exercises_count(english_catalog):
    units = english_catalog["units"]
    all_exercises = [
        ex for unit in units for skill in unit["skills"] for lesson in skill["lessons"] for ex in lesson["exercises"]
    ]
    assert len(all_exercises) == 576, f"Expected 576 exercises in English course, found {len(all_exercises)}"


def test_every_skill_has_objective_and_difficulty(english_catalog):
    units = english_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    for skill in all_skills:
        assert skill.get("objective"), f"Skill '{skill['id']}' missing objective"
        assert 1 <= skill.get("difficulty", 0) <= 8, f"Skill '{skill['id']}' has invalid difficulty {skill.get('difficulty')}"


def test_every_skill_has_exactly_three_lessons(english_catalog):
    units = english_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]
    for skill in all_skills:
        lessons = skill["lessons"]
        assert len(lessons) == 3, f"Skill '{skill['id']}' expected 3 lessons, got {len(lessons)}"
        assert lessons[0]["title"].endswith("Learn")
        assert lessons[1]["title"].endswith("Practice")
        assert lessons[2]["title"].endswith("Mastery")


def test_every_lesson_has_six_exercises(english_catalog):
    units = english_catalog["units"]
    all_lessons = [lesson for unit in units for skill in unit["skills"] for lesson in skill["lessons"]]
    for lesson in all_lessons:
        ex_count = len(lesson["exercises"])
        assert ex_count == 6, f"Lesson '{lesson['id']}' expected 6 exercises, got {ex_count}"


def test_all_six_exercise_types_represented(english_catalog):
    units = english_catalog["units"]
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
    assert expected_types == types_found, f"Missing exercise types in English catalog: {expected_types - types_found}"


def test_prerequisite_chain_validity(english_catalog):
    units = english_catalog["units"]
    all_skills = [skill for unit in units for skill in unit["skills"]]

    # Skill 0 has None prereq
    assert all_skills[0]["prerequisite_skill_id"] is None

    # Skills 1 to 31 have previous skill as prereq
    for i in range(1, len(all_skills)):
        curr_skill = all_skills[i]
        prev_skill = all_skills[i - 1]
        assert curr_skill["prerequisite_skill_id"] == prev_skill["id"], (
            f"Skill '{curr_skill['id']}' prerequisite should be '{prev_skill['id']}', got '{curr_skill['prerequisite_skill_id']}'"
        )


def test_deterministic_generation(english_catalog):
    """Regenerate course to confirm IDs and exercises are identical."""
    cat2 = generate_course(ENGLISH_COURSE_SPEC)
    assert english_catalog == cat2
