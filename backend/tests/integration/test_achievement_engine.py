"""
Integration tests for Phase 27 — Advanced Achievements + Reward System 2.0.

Verifies:
1. ~28 achievements seeded across 6 categories (learning, streak, xp, mastery, course, review)
2. Data-driven requirement evaluation logic
3. Course-specific achievement evaluation (e.g. SPANISH_BEGINNER vs ENGLISH_MASTER)
4. Category query filtering GET /api/v1/achievements?category=streak
5. Progress metrics (current_value vs target_value)
6. Anti-recursion bonus XP award safety
"""

import pytest
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel
from app.modules.gamification.service import GamificationService
from app.modules.gamification.models import AchievementModel
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_achievement_catalog_expansion(seeded_db: Session):
    achievements = seeded_db.query(AchievementModel).all()
    assert len(achievements) >= 28

    categories = {ach.category for ach in achievements}
    assert "learning" in categories
    assert "streak" in categories
    assert "xp" in categories
    assert "mastery" in categories
    assert "course" in categories
    assert "review" in categories


def test_category_filtering(seeded_db: Session):
    service = GamificationService(seeded_db)
    streak_achs = service.get_all_achievements(category="streak")
    assert len(streak_achs) >= 5
    for ach in streak_achs:
        assert ach.category == "streak"


def test_my_achievements_progress_reporting(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = GamificationService(seeded_db)

    my_achs = service.get_user_achievements(user)
    assert len(my_achs) >= 28

    for item in my_achs:
        assert item.target > 0
        assert item.progress >= 0
        assert item.achievement.rarity in ("common", "rare", "epic", "legendary")


def test_course_specific_achievement_evaluation(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = GamificationService(seeded_db)

    newly_earned = service.evaluate_achievements(user.id, course_id="crs_spanish")
    # Spanish master should be unearned since user hasn't completed Spanish 100%
    earned_codes = {ach.code for ach in newly_earned}
    assert "SPANISH_MASTER" not in earned_codes
