import pytest
from datetime import date, timedelta
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.progress.models import ExerciseAttemptModel, SkillProgressModel, DailyActivityModel
from app.modules.gamification.models import UserStatsModel, UserAchievementModel
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
async def test_get_user_profile_bff_endpoint(client: AsyncClient):
    response = await client.get("/api/v1/users/me/profile")
    assert response.status_code == 200
    data = response.json()

    assert "user" in data and data["user"]["id"] == "usr_demo"
    assert "stats" in data and data["stats"]["total_xp"] == 150
    assert "learning" in data
    assert "lessons_completed" in data["learning"]
    assert "skills_completed" in data["learning"]
    assert "course_progress_percent" in data["learning"]


@pytest.mark.asyncio
async def test_get_my_achievements_with_progress(client: AsyncClient):
    response = await client.get("/api/v1/users/me/achievements")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    first_ach = data[0]
    assert "achievement" in first_ach
    assert "is_earned" in first_ach
    assert "progress" in first_ach
    assert "target" in first_ach


@pytest.mark.asyncio
async def test_automated_achievement_evaluation_and_idempotency(db_session: Session):
    service = GamificationService(db_session)

    # Initially evaluate achievements
    newly = service.evaluate_achievements("usr_demo", commit=True)
    assert isinstance(newly, list)

    # Duplicate evaluation should return empty list (idempotency safety)
    dup = service.evaluate_achievements("usr_demo", commit=True)
    assert len(dup) == 0


@pytest.mark.asyncio
async def test_lesson_completion_returns_newly_earned_achievements(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

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

    comp_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert comp_res.status_code == 200
    data = comp_res.json()
    assert "achievements" in data
    assert "newly_earned" in data["achievements"]
