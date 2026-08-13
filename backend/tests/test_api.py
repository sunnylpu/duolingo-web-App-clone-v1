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
async def test_hearts_system_deduction_and_zero_hearts(client: AsyncClient, db_session: Session):
    # 1. Start lesson
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # 2. Correct answer -> hearts_lost: 0, hearts_remaining: 5
    correct_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Hello"},
    )
    assert correct_res.status_code == 200
    c_data = correct_res.json()
    assert c_data["is_correct"] is True
    assert c_data["hearts_lost"] == 0
    assert c_data["hearts_remaining"] == 5

    # 3. Duplicate submission -> no second heart deduction
    dup_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Hello"},
    )
    assert dup_res.status_code == 200
    assert dup_res.json()["hearts_remaining"] == 5

    # 4. Incorrect answer -> hearts_lost: 1, hearts_remaining: 4
    inc1_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_2/answer",
        json={"attempt_id": attempt_id, "answer": "Wrong Answer"},
    )
    assert inc1_res.status_code == 200
    inc1_data = inc1_res.json()
    assert inc1_data["is_correct"] is False
    assert inc1_data["hearts_lost"] == 1
    assert inc1_data["hearts_remaining"] == 4

    # Manually drain hearts in test DB to test 0 hearts state
    user_stats = db_session.query(UserStatsModel).filter(UserStatsModel.user_id == "usr_demo").first()
    assert user_stats is not None
    user_stats.hearts = 0
    db_session.commit()

    # 5. Answer submission with 0 hearts -> HTTP 409 OUT_OF_HEARTS
    start2_res = await client.post("/api/v1/lessons/lsn_greetings_2/start")
    attempt2_id = start2_res.json()["attempt_id"]

    zero_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_2/exercises/ex_gr2_2/answer",
        json={"attempt_id": attempt2_id, "answer": "Por favor"},
    )
    assert zero_res.status_code == 409
    z_data = zero_res.json()
    assert z_data["error"]["code"] == "OUT_OF_HEARTS"


@pytest.mark.asyncio
async def test_answer_validation_security_mismatches(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    mismatch_ex_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr2_2/answer",
        json={"attempt_id": attempt_id, "answer": "Por favor"},
    )
    assert mismatch_ex_res.status_code == 400
