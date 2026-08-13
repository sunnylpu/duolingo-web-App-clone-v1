import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.progress.models import ExerciseAttemptModel, SkillProgressModel, DailyActivityModel
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
    assert data["hearts"] == 5


@pytest.mark.asyncio
async def test_list_courses(client: AsyncClient):
    response = await client.get("/api/v1/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_course_detail(client: AsyncClient):
    response = await client.get("/api/v1/courses/crs_spanish")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "crs_spanish"


@pytest.mark.asyncio
async def test_get_learning_path(client: AsyncClient):
    response = await client.get("/api/v1/path")
    assert response.status_code == 200
    data = response.json()
    assert "units" in data


@pytest.mark.asyncio
async def test_full_lesson_completion_xp_and_idempotency(client: AsyncClient, db_session: Session):
    # 1. Start lesson lsn_greetings_1 (has 6 exercises: ex_gr1_1 .. ex_gr1_6)
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # 2. Answer all 6 exercises correctly
    answers = [
        ("ex_gr1_1", "Hello"),
        ("ex_gr1_2", "Good morning"),
        ("ex_gr1_3", {"pairs": [["Hola", "Hello"], ["Gracias", "Thank you"], ["Adiós", "Goodbye"]]}),
        ("ex_gr1_4", "Buenas noches"),
        ("ex_gr1_5", "Hasta luego"),
        ("ex_gr1_6", "como"),
    ]

    for ex_id, ans in answers:
        ans_res = await client.post(
            f"/api/v1/lessons/lsn_greetings_1/exercises/{ex_id}/answer",
            json={"attempt_id": attempt_id, "answer": ans},
        )
        assert ans_res.status_code == 200
        assert ans_res.json()["is_correct"] is True

    # 3. Call lesson completion endpoint
    comp_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert comp_res.status_code == 200
    c_data = comp_res.json()
    assert c_data["status"] == "completed"
    assert c_data["xp_earned"] == 10
    assert c_data["score"] == 100
    assert c_data["already_completed"] is False
    assert c_data["skill_progress"]["crown_level"] >= 1

    # Verify UserStats total_xp increased from 150 to 160
    stats = db_session.query(UserStatsModel).filter(UserStatsModel.user_id == "usr_demo").first()
    assert stats is not None
    assert stats.total_xp == 160

    # 4. Repeat completion request (Idempotency test)
    dup_comp = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert dup_comp.status_code == 200
    dup_data = dup_comp.json()
    assert dup_data["status"] == "completed"
    assert dup_data["xp_earned"] == 0  # No duplicate XP
    assert dup_data["already_completed"] is True

    # Verify total_xp remains 160
    db_session.refresh(stats)
    assert stats.total_xp == 160


@pytest.mark.asyncio
async def test_incomplete_lesson_completion_rejection(client: AsyncClient):
    # Start lesson lsn_greetings_2 (has 2 exercises: ex_gr2_1, ex_gr2_2)
    start_res = await client.post("/api/v1/lessons/lsn_greetings_2/start")
    attempt_id = start_res.json()["attempt_id"]

    # Answer only 1 exercise out of 2
    ans_res = await client.post(
        "/api/v1/lessons/lsn_greetings_2/exercises/ex_gr2_1/answer",
        json={"attempt_id": attempt_id, "answer": "Muchas gracias"},
    )
    assert ans_res.status_code == 200

    # Attempt completing incomplete lesson -> HTTP 400 LESSON_NOT_COMPLETE
    comp_res = await client.post(
        "/api/v1/lessons/lsn_greetings_2/complete",
        json={"attempt_id": attempt_id},
    )
    assert comp_res.status_code == 400
    assert comp_res.json()["error"]["message"] == "Not all exercises have been answered."
