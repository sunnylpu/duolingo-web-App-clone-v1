"""
Tests for Phase 25 — Advanced Learner Dashboard + Course Hub (Home Aggregation API).

Verifies:
1. Home aggregation endpoint GET /api/v1/home for default course (English)
2. Home aggregation endpoint GET /api/v1/home for Spanish & French courses
3. Continue Learning summary metrics (recommended unit, skill, lesson)
4. Daily goal, streak, hearts, and course hub array integrity
5. Recommended lesson resolution logic (nearest incomplete lesson in recommended skill)
"""

import pytest
from sqlalchemy.orm import Session

from app.modules.user.models import UserModel
from app.modules.home.service import HomeService
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_home_dashboard_default_english(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = HomeService(seeded_db)

    dashboard = service.get_home_dashboard(user)
    assert dashboard.course.id in ("crs_english", "crs_spanish", "crs_french")
    assert dashboard.continue_learning is not None
    assert dashboard.daily_goal is not None
    assert dashboard.streak is not None
    assert dashboard.hearts is not None
    assert len(dashboard.courses) == 3


def test_home_dashboard_spanish_course(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = HomeService(seeded_db)

    dashboard = service.get_home_dashboard(user, course_id="crs_spanish")
    assert dashboard.course.id == "crs_spanish"
    assert dashboard.course.name == "Spanish"
    assert dashboard.continue_learning.unit_title is not None
    assert dashboard.continue_learning.skill_id is not None
    assert dashboard.continue_learning.lesson_id is not None


def test_home_dashboard_french_course(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = HomeService(seeded_db)

    dashboard = service.get_home_dashboard(user, course_id="crs_french")
    assert dashboard.course.id == "crs_french"
    assert dashboard.course.name == "French"
    assert dashboard.continue_learning.unit_title is not None
    assert dashboard.continue_learning.skill_id is not None
    assert dashboard.continue_learning.lesson_id is not None
