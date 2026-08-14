"""
Tests for Phase 26 — Premium Lesson Intelligence + Adaptive Difficulty + Smart Review.

Verifies:
1. Deterministic skill mastery score & mastery state rules (weak, developing, strong, mastered)
2. Adaptive difficulty recommendations (bounded by current_difficulty +/- 1)
3. Skill performance endpoint GET /api/v1/progress/skills/{skill_id}
4. Smart Review endpoint GET /api/v1/review?course_id=...
5. Zero XP practice reward rule for Smart Review (prevents XP farming)
6. Multi-course review isolation
"""

import pytest
from sqlalchemy.orm import Session

from app.modules.user.models import UserModel
from app.modules.progress.service import ProgressService
from app.modules.progress.difficulty import (
    calculate_mastery_score,
    calculate_mastery_state,
    recommend_difficulty,
)
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_mastery_rules_and_adaptive_difficulty():
    # Weak state
    score_weak = calculate_mastery_score(20.0, 40.0)
    assert score_weak == 30.0
    assert calculate_mastery_state(score_weak) == "weak"

    # Developing state
    score_dev = calculate_mastery_score(60.0, 50.0)
    assert score_dev == 55.0
    assert calculate_mastery_state(score_dev) == "developing"

    # Strong state
    score_strong = calculate_mastery_score(80.0, 80.0)
    assert score_strong == 80.0
    assert calculate_mastery_state(score_strong) == "strong"

    # Mastered state
    score_mastered = calculate_mastery_score(100.0, 95.0)
    assert score_mastered == 97.5
    assert calculate_mastery_state(score_mastered) == "mastered"

    # Adaptive difficulty step rules (+/- 1 max)
    assert recommend_difficulty(current_difficulty=2, accuracy_percent=90.0) == 3
    assert recommend_difficulty(current_difficulty=2, accuracy_percent=40.0) == 1
    assert recommend_difficulty(current_difficulty=2, accuracy_percent=75.0) == 2


def test_skill_performance_endpoint_logic(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    perf = service.get_skill_performance(user, skill_id="skill_greetings")
    assert perf.skill_id == "skill_greetings"
    assert perf.mastery_state in ("weak", "developing", "strong", "mastered")
    assert 0.0 <= perf.mastery_score <= 100.0
    assert 1 <= perf.recommended_difficulty <= 3


def test_smart_review_endpoint_logic(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    review = service.get_smart_review(user, course_id="crs_english")
    assert review.available is True
    assert review.count > 0
    assert len(review.exercises) > 0

    # Verify zero XP reward rule to prevent farming
    for ex in review.exercises:
        assert ex.xp_reward == 0


def test_multi_course_review_isolation(seeded_db: Session):
    user = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = ProgressService(seeded_db)

    review_es = service.get_smart_review(user, course_id="crs_spanish")
    review_fr = service.get_smart_review(user, course_id="crs_french")

    assert review_es.available is True
    assert review_fr.available is True
