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
    assert len(data["exercises"]) == 6  # All 6 exercise types in lsn_greetings_1


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
async def test_match_pairs_exercise_validation(client: AsyncClient, db_session: Session):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    # 1. Correct Match Pairs (ex_gr1_3) with reordered list
    mp_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_3/answer",
        json={
            "attempt_id": attempt_id,
            "answer": {
                "pairs": [
                    ["Adiós", "Goodbye"],
                    ["Hola", "Hello"],
                    ["Gracias", "Thank you"],
                ]
            },
        },
    )
    assert mp_res.status_code == 200
    mp_data = mp_res.json()
    assert mp_data["is_correct"] is True
    assert mp_data["hearts_lost"] == 0

    # 2. Incorrect Match Pairs (wrong pairing) on another lesson attempt for lsn_greetings_1
    start2_res = await client.post("/api/v1/lessons/lsn_greetings_2/start")
    attempt2_id = start2_res.json()["attempt_id"]

    mp_inc_res = await client.post(
        "/api/v1/lessons/lsn_greetings_2/exercises/ex_gr2_1/answer",
        json={
            "attempt_id": attempt2_id,
            "answer": {
                "pairs": [
                    ["Muchas", "de nada"],  # Wrong pair
                ]
            },
        },
    )
    assert mp_inc_res.status_code == 200
    assert mp_inc_res.json()["is_correct"] is False
    assert mp_inc_res.json()["hearts_lost"] == 1


@pytest.mark.asyncio
async def test_fill_blank_exercise_validation(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    # 1. Correct Fill Blank (ex_gr1_6: correct "como")
    fb_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_6/answer",
        json={"attempt_id": attempt_id, "answer": "  COMO  "},
    )
    assert fb_res.status_code == 200
    fb_data = fb_res.json()
    assert fb_data["is_correct"] is True
    assert fb_data["correct_answer"] == "como"
    assert fb_data["hearts_lost"] == 0

    # 2. Incorrect Fill Blank
    fb_inc_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_4/answer",
        json={"attempt_id": attempt_id, "answer": "Wrong Word"},
    )
    assert fb_inc_res.status_code == 200
    assert fb_inc_res.json()["is_correct"] is False
    assert fb_inc_res.json()["hearts_lost"] == 1


@pytest.mark.asyncio
async def test_all_six_exercise_types_full_regression(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    # Type 1: multiple_choice (ex_gr1_1)
    res1 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Hello"},
    )
    assert res1.status_code == 200 and res1.json()["is_correct"] is True

    # Type 2: translate (ex_gr1_2)
    res2 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_2/answer",
        json={"attempt_id": attempt_id, "answer": "Good morning"},
    )
    assert res2.status_code == 200 and res2.json()["is_correct"] is True

    # Type 3: match_pairs (ex_gr1_3)
    res3 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_3/answer",
        json={
            "attempt_id": attempt_id,
            "answer": {
                "pairs": [
                    ["Hola", "Hello"],
                    ["Gracias", "Thank you"],
                    ["Adiós", "Goodbye"],
                ]
            },
        },
    )
    assert res3.status_code == 200 and res3.json()["is_correct"] is True

    # Type 4: type_answer (ex_gr1_4)
    res4 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_4/answer",
        json={"attempt_id": attempt_id, "answer": "Buenas noches"},
    )
    assert res4.status_code == 200 and res4.json()["is_correct"] is True

    # Type 5: word_bank (ex_gr1_5)
    res5 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_5/answer",
        json={"attempt_id": attempt_id, "answer": "Hasta luego"},
    )
    assert res5.status_code == 200 and res5.json()["is_correct"] is True

    # Type 6: fill_blank (ex_gr1_6)
    res6 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_6/answer",
        json={"attempt_id": attempt_id, "answer": "como"},
    )
    assert res6.status_code == 200 and res6.json()["is_correct"] is True


@pytest.mark.asyncio
async def test_answer_validation_security_mismatches(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    mismatch_ex_res = await client.post(
        f"/api/v1/lessons/lsn_greetings_1/exercises/ex_gr2_2/answer",
        json={"attempt_id": attempt_id, "answer": "Por favor"},
    )
    assert mismatch_ex_res.status_code == 400
