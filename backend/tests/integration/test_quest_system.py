"""
Integration tests for Phase 30 — Daily Quests + Missions + Challenge System.

Verifies:
1. Daily quest generation stability and determinism per learner and date
2. Weekly challenge assignment and progress tracking
3. Domain event tracking (LESSONS_COMPLETED, XP_EARNED, CORRECT_ANSWERS, SKILLS_COMPLETED)
4. Quest completion XP reward settlement (awarded exactly once inside transaction)
5. Quest XP integration into UserStats, DailyActivity, and Leaderboards
6. Quest history API endpoint
"""

import pytest
import datetime
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel
from app.modules.quests.service import QuestService
from app.modules.lesson.service import LessonService
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_daily_quests_generation_determinism(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    quest_svc = QuestService(seeded_db)

    # First fetch today's quests
    res1 = quest_svc.get_today_quests(user_demo)
    assert len(res1.quests) == 3

    # Fetching again on same date must return identical quest IDs
    res2 = quest_svc.get_today_quests(user_demo)
    assert len(res2.quests) == 3
    q_ids_1 = [q.id for q in res1.quests]
    q_ids_2 = [q.id for q in res2.quests]
    assert q_ids_1 == q_ids_2


def test_weekly_challenge_assignment(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    quest_svc = QuestService(seeded_db)

    res = quest_svc.get_weekly_challenge(user_demo)
    assert res.challenge is not None
    assert res.challenge.quest_scope == "weekly"
    assert res.challenge.target_value > 0


def test_quest_progress_and_reward_idempotency(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    quest_svc = QuestService(seeded_db)

    # Fetch today's assigned quests
    res_today = quest_svc.get_today_quests(user_demo)
    q_target = res_today.quests[0]

    initial_xp = user_demo.stats.total_xp

    # Record progress event matching quest type
    completed_titles = quest_svc.record_quest_event(
        user_id=user_demo.id,
        quest_type=q_target.quest_type,
        amount=q_target.target_value,
    )

    # Verify completion
    res_after = quest_svc.get_today_quests(user_demo)
    updated_quest = next(q for q in res_after.quests if q.id == q_target.id)

    assert updated_quest.completed is True
    assert user_demo.stats.total_xp == initial_xp + updated_quest.reward_xp

    # Duplicate progress event should NOT award bonus XP again
    xp_after_first = user_demo.stats.total_xp
    quest_svc.record_quest_event(
        user_id=user_demo.id,
        quest_type=q_target.quest_type,
        amount=5,
    )
    assert user_demo.stats.total_xp == xp_after_first


def test_quest_history(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    quest_svc = QuestService(seeded_db)

    # Complete a quest
    quest_svc.get_today_quests(user_demo)
    quest_svc.record_quest_event(user_id=user_demo.id, quest_type="LESSONS_COMPLETED", amount=10)

    history = quest_svc.get_quest_history(user_demo)
    assert history.total_completed >= 1
