import pytest
from datetime import datetime, timezone, timedelta
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.shared.clock import MockClock
from app.modules.gamification.service import GamificationService
from app.modules.gamification.models import UserStatsModel


@pytest.fixture(autouse=True)
def setup_seed_data(db_session: Session):
    """Seed test database before API test execution."""
    seed_database(db_session)


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_lazy_heart_regeneration_with_mock_clock(db_session: Session):
    start_time = datetime(2026, 8, 13, 10, 0, 0, tzinfo=timezone.utc)
    mock_clock = MockClock(start_time)
    service = GamificationService(db_session, clock=mock_clock)

    # 1. Set user hearts to 2
    stats = service.repository.get_user_stats("usr_demo")
    stats.hearts = 2
    stats.last_heart_regeneration_at = start_time
    db_session.commit()

    # 2. Advance clock by 30 minutes (1 interval) -> 3 hearts
    mock_clock.advance(minutes=30)
    refreshed = service.refresh_hearts("usr_demo")
    assert refreshed.hearts == 3

    # 3. Advance clock by 90 minutes (3 intervals) -> 5 hearts (capped at 5/5)
    mock_clock.advance(minutes=90)
    refreshed2 = service.refresh_hearts("usr_demo")
    assert refreshed2.hearts == 5
    assert refreshed2.last_heart_regeneration_at is None


@pytest.mark.asyncio
async def test_out_of_hearts_exercise_submission_rejection(client: AsyncClient, db_session: Session):
    service = GamificationService(db_session)
    stats = service.repository.get_user_stats("usr_demo")
    stats.hearts = 0
    stats.last_heart_regeneration_at = service.clock.now()
    db_session.commit()

    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    att_id = start_res.json()["attempt_id"]

    # Submit answer with 0 hearts -> HTTP 409 OUT_OF_HEARTS
    ans_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": att_id, "answer": "WrongAnswer"},
    )
    assert ans_res.status_code == 409
    assert ans_res.json()["error"]["code"] == "OUT_OF_HEARTS"


@pytest.mark.asyncio
async def test_practice_recovery_and_cooldown(client: AsyncClient, db_session: Session):
    service = GamificationService(db_session)
    stats = service.repository.get_user_stats("usr_demo")
    stats.hearts = 2
    stats.last_practice_recovery_at = None
    db_session.commit()

    # Get practice exercise
    ex_res = await client.get("/api/v1/gamification/practice")
    assert ex_res.status_code == 200
    ex_data = ex_res.json()
    assert "exercise_id" in ex_data

    # Submit correct practice answer -> +1 heart (2 -> 3)
    sub_res = await client.post(
        "/api/v1/gamification/practice",
        json={"exercise_id": ex_data["exercise_id"], "answer": ex_data["correct_answer"]},
    )
    assert sub_res.status_code == 200
    assert sub_res.json()["hearts"] == 3
    assert sub_res.json()["recovered"] == 1

    # Immediate second practice attempt -> HTTP 400 PRACTICE_COOLDOWN
    sub_res2 = await client.post(
        "/api/v1/gamification/practice",
        json={"exercise_id": ex_data["exercise_id"], "answer": ex_data["correct_answer"]},
    )
    assert sub_res2.status_code == 400
    assert sub_res2.json()["error"]["code"] == "PRACTICE_COOLDOWN"


@pytest.mark.asyncio
async def test_mock_heart_refill(client: AsyncClient, db_session: Session):
    service = GamificationService(db_session)
    stats = service.repository.get_user_stats("usr_demo")
    stats.hearts = 1
    db_session.commit()

    refill_res = await client.post("/api/v1/gamification/hearts/refill")
    assert refill_res.status_code == 200
    assert refill_res.json()["hearts"] == 5
    assert refill_res.json()["refilled"] is True
