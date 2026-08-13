import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.progress.models import ExerciseAttemptModel
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
    assert data["username"] == "demolearner"


@pytest.mark.asyncio
async def test_get_user_stats(client: AsyncClient):
    response = await client.get("/api/v1/users/me/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_xp"] == 150
    assert data["current_streak"] == 7
    assert data["hearts"] == 5


@pytest.mark.asyncio
async def test_list_courses(client: AsyncClient):
    response = await client.get("/api/v1/courses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["code"] == "es"


@pytest.mark.asyncio
async def test_get_course_detail_and_404(client: AsyncClient):
    response = await client.get("/api/v1/courses/crs_spanish")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "crs_spanish"

    err_res = await client.get("/api/v1/courses/invalid_course_id")
    assert err_res.status_code == 404


@pytest.mark.asyncio
async def test_get_learning_path(client: AsyncClient):
    response = await client.get("/api/v1/path")
    assert response.status_code == 200
    data = response.json()
    assert "course" in data
    assert "units" in data


@pytest.mark.asyncio
async def test_get_lesson_detail_and_404(client: AsyncClient):
    response = await client.get("/api/v1/lessons/lsn_greetings_1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "lsn_greetings_1"

    err_res = await client.get("/api/v1/lessons/invalid_lesson_id")
    assert err_res.status_code == 404


@pytest.mark.asyncio
async def test_start_lesson_endpoint_and_reuse(client: AsyncClient):
    response = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert response.status_code == 200
    data = response.json()
    assert "attempt_id" in data
    attempt_id_1 = data["attempt_id"]

    res_reuse = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert res_reuse.status_code == 200
    assert res_reuse.json()["attempt_id"] == attempt_id_1


@pytest.mark.asyncio
async def test_translate_and_word_bank_exercise_validation(client: AsyncClient, db_session: Session):
    # 1. Start lesson lsn_greetings_1 (contains ex_gr1_2: translate)
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # 2. Correct Translate Answer ("ex_gr1_2": correct "Good morning")
    trans_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_2/answer",
        json={"attempt_id": attempt_id, "answer": "  good MORNING.  "},
    )
    assert trans_res.status_code == 200
    t_data = trans_res.json()
    assert t_data["is_correct"] is True
    assert t_data["correct_answer"] == "Good morning"
    assert t_data["hearts_lost"] == 0

    # 3. Incorrect Translate Answer ("ex_gr1_1": MCQ prompt)
    trans_inc = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Wrong Translation"},
    )
    assert trans_inc.status_code == 200
    assert trans_inc.json()["is_correct"] is False
    assert trans_inc.json()["hearts_lost"] == 1
    assert trans_inc.json()["hearts_remaining"] == 4

    # 4. Start lesson lsn_greetings_2 (contains ex_gr2_1: word_bank "Muchas gracias")
    start2_res = await client.post("/api/v1/lessons/lsn_greetings_2/start")
    attempt2_id = start2_res.json()["attempt_id"]

    # Correct Word Bank assembled string ("Muchas gracias")
    wb_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_2/exercises/ex_gr2_1/answer",
        json={"attempt_id": attempt2_id, "answer": "Muchas gracias"},
    )
    assert wb_res.status_code == 200
    wb_data = wb_res.json()
    assert wb_data["is_correct"] is True
    assert wb_data["hearts_lost"] == 0

    # Incorrect Word Bank ordering ("gracias Muchas")
    wb_inc_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_2/exercises/ex_gr2_2/answer",
        json={"attempt_id": attempt2_id, "answer": "Wrong Word Order"},
    )
    assert wb_inc_res.status_code == 200
    assert wb_inc_res.json()["is_correct"] is False
    assert wb_inc_res.json()["hearts_lost"] == 1
    assert wb_inc_res.json()["hearts_remaining"] == 3


@pytest.mark.asyncio
async def test_answer_validation_security_mismatches(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    mismatch_ex_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr2_2/answer",
        json={"attempt_id": attempt_id, "answer": "Por favor"},
    )
    assert mismatch_ex_res.status_code == 400
