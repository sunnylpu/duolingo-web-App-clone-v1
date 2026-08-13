import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.progress.models import ExerciseAttemptModel


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
    assert len(data["units"]) == 3

    err_res = await client.get("/api/v1/courses/invalid_course_id")
    assert err_res.status_code == 404
    err_data = err_res.json()
    assert err_data["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_get_learning_path(client: AsyncClient):
    response = await client.get("/api/v1/path")
    assert response.status_code == 200
    data = response.json()
    assert "course" in data
    assert "units" in data
    assert len(data["units"]) == 3


@pytest.mark.asyncio
async def test_get_lesson_detail_and_404(client: AsyncClient):
    response = await client.get("/api/v1/lessons/lsn_greetings_1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "lsn_greetings_1"
    assert len(data["exercises"]) > 0

    err_res = await client.get("/api/v1/lessons/invalid_lesson_id")
    assert err_res.status_code == 404


@pytest.mark.asyncio
async def test_start_lesson_endpoint_and_reuse(client: AsyncClient):
    response = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert response.status_code == 200
    data = response.json()
    assert "attempt_id" in data
    assert data["lesson_id"] == "lsn_greetings_1"
    assert data["status"] == "started"
    attempt_id_1 = data["attempt_id"]

    res_reuse = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert res_reuse.status_code == 200
    assert res_reuse.json()["attempt_id"] == attempt_id_1


@pytest.mark.asyncio
async def test_answer_validation_mcq_and_type_answer(client: AsyncClient, db_session: Session):
    # 1. Start lesson lsn_greetings_1
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # 2. Correct MCQ Answer ("ex_gr1_1": correct "Hello")
    mcq_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Hello"},
    )
    assert mcq_res.status_code == 200
    mcq_data = mcq_res.json()
    assert mcq_data["is_correct"] is True
    assert mcq_data["correct_answer"] == "Hello"
    assert mcq_data["hearts_lost"] == 0

    # Verify ExerciseAttempt record in database
    ex_attempt = (
        db_session.query(ExerciseAttemptModel)
        .filter(ExerciseAttemptModel.exercise_id == "ex_gr1_1")
        .first()
    )
    assert ex_attempt is not None
    assert ex_attempt.is_correct is True

    # 3. Duplicate submission prevention
    dup_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Hello"},
    )
    assert dup_res.status_code == 400
    assert dup_res.json()["error"]["message"] == "EXERCISE_ALREADY_ANSWERED"

    # 4. Incorrect MCQ answer submission ("ex_gr1_2": correct "Good morning")
    inc_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_2/answer",
        json={"attempt_id": attempt_id, "answer": "Wrong Answer"},
    )
    assert inc_res.status_code == 200
    inc_data = inc_res.json()
    assert inc_data["is_correct"] is False
    assert inc_data["correct_answer"] == "Good morning"
    assert inc_data["hearts_lost"] == 0

    # 5. Type Answer validation on lsn_greetings_2 ("ex_gr2_2": correct "Por favor")
    start2_res = await client.post("/api/v1/lessons/lsn_greetings_2/start")
    attempt_id_2 = start2_res.json()["attempt_id"]

    type_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_2/exercises/ex_gr2_2/answer",
        json={"attempt_id": attempt_id_2, "answer": "  por FAVOR  "},
    )
    assert type_res.status_code == 200
    assert type_res.json()["is_correct"] is True


@pytest.mark.asyncio
async def test_answer_validation_security_mismatches(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    # Exercise ex_gr2_2 belongs to lesson lsn_greetings_2, NOT lsn_greetings_1
    mismatch_ex_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr2_2/answer",
        json={"attempt_id": attempt_id, "answer": "Por favor"},
    )
    assert mismatch_ex_res.status_code == 400
