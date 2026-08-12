import pytest
from datetime import date
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.shared.database import init_db
from app.modules.user.models import UserModel
from app.modules.course.models import CourseModel, UnitModel
from app.modules.lesson.models import SkillModel, LessonModel, ExerciseModel
from app.modules.progress.models import (
    SkillProgressModel,
    LessonAttemptModel,
    ExerciseAttemptModel,
    DailyActivityModel,
)
from app.modules.gamification.models import (
    UserStatsModel,
    AchievementModel,
    UserAchievementModel,
)
from app.modules.leaderboard.models import LeaderboardEntryModel
from seed.seed import seed_database


def test_database_initialization(db_session: Session):
    """Verify all 14 domain tables are created properly."""
    init_db(target_engine=db_session.bind)
    tables = [
        "users",
        "courses",
        "units",
        "skills",
        "lessons",
        "exercises",
        "user_stats",
        "skill_progress",
        "lesson_attempts",
        "exercise_attempts",
        "daily_activities",
        "achievements",
        "user_achievements",
        "leaderboard_entries",
    ]
    for table in tables:
        result = db_session.execute(
            text(f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table}'")
        ).scalar()
        assert result == 1, f"Table {table} does not exist"


def test_user_creation_and_stats_relationship(db_session: Session):
    """Verify User creation and 1-to-1 UserStats relationship."""
    user = UserModel(
        id="usr_test1",
        username="testuser",
        display_name="Test User",
        email="test@example.com",
    )
    stats = UserStatsModel(
        id="stats_test1",
        user_id="usr_test1",
        total_xp=100,
        current_streak=3,
    )
    db_session.add(user)
    db_session.add(stats)
    db_session.commit()

    fetched_user = db_session.query(UserModel).filter_by(id="usr_test1").first()
    assert fetched_user is not None
    assert fetched_user.stats is not None
    assert fetched_user.stats.total_xp == 100
    assert fetched_user.stats.current_streak == 3


def test_course_unit_skill_lesson_exercise_hierarchy(db_session: Session):
    """Verify Course -> Unit -> Skill -> Lesson -> Exercise relational cascade hierarchy."""
    course = CourseModel(
        id="crs_fr",
        name="French",
        code="fr",
        source_language="en",
        target_language="fr",
    )
    unit = UnitModel(id="unit_fr_1", course_id="crs_fr", title="Unit 1", order_index=1)
    skill = SkillModel(id="skill_fr_1", unit_id="unit_fr_1", title="Greetings", order_index=1)
    lesson = LessonModel(id="lsn_fr_1", skill_id="skill_fr_1", title="Lesson 1", order_index=1)
    exercise = ExerciseModel(
        id="ex_fr_1",
        lesson_id="lsn_fr_1",
        type="multiple_choice",
        prompt="What does 'Bonjour' mean?",
        correct_answer="Hello",
        data={"options": ["Hello", "Bye"]},
        order_index=1,
    )

    db_session.add_all([course, unit, skill, lesson, exercise])
    db_session.commit()

    fetched_course = db_session.query(CourseModel).filter_by(id="crs_fr").first()
    assert len(fetched_course.units) == 1
    assert fetched_course.units[0].skills[0].title == "Greetings"
    assert fetched_course.units[0].skills[0].lessons[0].exercises[0].correct_answer == "Hello"


def test_prerequisite_skill_relationship(db_session: Session):
    """Verify self-referencing prerequisite skill relationship."""
    course = CourseModel(id="crs_es", name="Spanish", code="es", source_language="en", target_language="es")
    unit = UnitModel(id="unit_es_1", course_id="crs_es", title="Unit 1", order_index=1)
    skill1 = SkillModel(id="skill_base", unit_id="unit_es_1", title="Basics", order_index=1)
    skill2 = SkillModel(
        id="skill_adv",
        unit_id="unit_es_1",
        title="Advanced",
        order_index=2,
        prerequisite_skill_id="skill_base",
    )

    db_session.add_all([course, unit, skill1, skill2])
    db_session.commit()

    adv_skill = db_session.query(SkillModel).filter_by(id="skill_adv").first()
    assert adv_skill.prerequisite_skill is not None
    assert adv_skill.prerequisite_skill.title == "Basics"


def test_unique_constraints(db_session: Session):
    """Verify unique constraints on SkillProgress, DailyActivity, and UserAchievement."""
    user = UserModel(id="usr_u1", username="u1", display_name="U1", email="u1@test.com")
    course = CourseModel(id="crs_u", name="Course", code="c1", source_language="en", target_language="es")
    unit = UnitModel(id="unit_u", course_id="crs_u", title="Unit 1", order_index=1)
    skill = SkillModel(id="skill_u", unit_id="unit_u", title="Skill 1", order_index=1)
    achievement = AchievementModel(
        id="ach_u", code="TEST_ACH", name="Ach", description="Desc", icon="icon", requirement_type="xp", requirement_value=10
    )
    db_session.add_all([user, course, unit, skill, achievement])
    db_session.commit()

    # 1. Unique SkillProgress constraint
    sp1 = SkillProgressModel(id="sp1", user_id="usr_u1", skill_id="skill_u")
    sp2 = SkillProgressModel(id="sp2", user_id="usr_u1", skill_id="skill_u")
    db_session.add(sp1)
    db_session.commit()

    db_session.add(sp2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # 2. Unique DailyActivity constraint
    d1 = DailyActivityModel(id="da1", user_id="usr_u1", activity_date=date(2026, 8, 12))
    d2 = DailyActivityModel(id="da2", user_id="usr_u1", activity_date=date(2026, 8, 12))
    db_session.add(d1)
    db_session.commit()

    db_session.add(d2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # 3. Unique UserAchievement constraint
    ua1 = UserAchievementModel(id="ua1", user_id="usr_u1", achievement_id="ach_u")
    ua2 = UserAchievementModel(id="ua2", user_id="usr_u1", achievement_id="ach_u")
    db_session.add(ua1)
    db_session.commit()

    db_session.add(ua2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()


def test_seed_execution_and_content(db_session: Session):
    """Verify seed execution populates all required entities cleanly."""
    counts = seed_database(db_session)
    assert counts["courses"] == 1
    assert counts["units"] == 3
    assert counts["skills"] == 6
    assert counts["lessons"] >= 6
    assert counts["exercises"] >= 6

    # Verify exercise types cover all 6 types
    exercises = db_session.query(ExerciseModel).all()
    types_found = {ex.type for ex in exercises}
    expected_types = {
        "multiple_choice",
        "translate",
        "word_bank",
        "match_pairs",
        "fill_blank",
        "type_answer",
    }
    assert expected_types.issubset(types_found), f"Missing exercise types: {expected_types - types_found}"

    # Verify demo learner user stats and progress
    demo = db_session.query(UserModel).filter_by(id="usr_demo").first()
    assert demo is not None
    assert demo.stats is not None
    assert demo.stats.current_streak == 7
    assert len(demo.user_achievements) >= 2
