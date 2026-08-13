import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.progress.models import ExerciseAttemptModel, SkillProgressModel, DailyActivityModel
from app.modules.gamification.models import UserStatsModel
from app.modules.gamification.service import GamificationService


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
async def test_get_current_user_me(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "usr_demo"


@pytest.mark.asyncio
async def test_get_user_stats(client: AsyncClient):
    response = await client.get("/api/v1/users/me/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_xp"] == 150
    assert data["current_streak"] == 7
    assert data["daily_goal_xp"] == 20


@pytest.mark.asyncio
async def test_get_today_activity(client: AsyncClient):
    response = await client.get("/api/v1/gamification/daily")
    assert response.status_code == 200
    data = response.json()
    assert "date" in data
    assert "xp_earned" in data
    assert "lessons_completed" in data
    assert "goal_xp" in data
    assert "goal_completed" in data


@pytest.mark.asyncio
async def test_streak_calculation_rules(db_session: Session):
    service = GamificationService(db_session)
    stats = db_session.query(UserStatsModel).filter(UserStatsModel.user_id == "usr_demo").first()
    assert stats is not None

    today = date(2026, 8, 13)
    yesterday = date(2026, 8, 12)
    two_days_ago = date(2026, 8, 11)

    # 1. First activity ever (last_active_date is None)
    stats.last_active_date = None
    stats.current_streak = 0
    stats.longest_streak = 0
    res1 = service.update_streak_and_daily_goal("usr_demo", 10, activity_date_override=today)
    assert res1["streak"]["current"] == 1
    assert res1["streak"]["longest"] == 1
    assert res1["streak"]["increased"] is True

    # 2. Same-day activity (last_active_date == today)
    res2 = service.update_streak_and_daily_goal("usr_demo", 10, activity_date_override=today)
    assert res2["streak"]["current"] == 1
    assert res2["streak"]["increased"] is False

    # 3. Consecutive day (last_active_date == yesterday)
    stats.last_active_date = yesterday
    res3 = service.update_streak_and_daily_goal("usr_demo", 10, activity_date_override=today)
    assert res3["streak"]["current"] == 2
    assert res3["streak"]["longest"] == 2
    assert res3["streak"]["increased"] is True

    # 4. Missed day (last_active_date == two_days_ago -> reset to 1)
    stats.last_active_date = two_days_ago - timedelta(days=1)
    res4 = service.update_streak_and_daily_goal("usr_demo", 10, activity_date_override=today)
    assert res4["streak"]["current"] == 1
    assert res4["streak"]["longest"] == 2  # Longest streak maintained!


@pytest.mark.asyncio
async def test_full_lesson_completion_streak_and_daily_goal(client: AsyncClient, db_session: Session):
    # Start lesson lsn_greetings_1
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    # Answer all 6 exercises
    answers = [
        ("ex_gr1_1", "Hello"),
        ("ex_gr1_2", "Good morning"),
        ("ex_gr1_3", {"pairs": [["Hola", "Hello"], ["Gracias", "Thank you"], ["Adiós", "Goodbye"]]}),
        ("ex_gr1_4", "Buenas noches"),
        ("ex_gr1_5", "Hasta luego"),
        ("ex_gr1_6", "como"),
    ]

    for ex_id, ans in answers:
        await client.post(
            f"/api/v1/lessons/lsn_greetings_1/exercises/{ex_id}/answer",
            json={"attempt_id": attempt_id, "answer": ans},
        )

    # Complete lesson
    comp_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert comp_res.status_code == 200
    c_data = comp_res.json()
    assert "streak" in c_data
    assert "daily_progress" in c_data
    assert c_data["streak"]["current"] >= 1

    # Idempotent repeat completion -> streak does not increment twice
    dup_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert dup_res.status_code == 200
    assert dup_res.json()["xp_earned"] == 0
