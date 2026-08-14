import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database


@pytest.fixture(autouse=True)
def setup_seed_data(db_session: Session):
    """Seed test database before integration test execution."""
    seed_database(db_session)


@pytest.mark.asyncio
async def test_duplicate_answer_submission_retry_idempotency(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    # Initial submission
    ans1 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Hola"},
    )
    assert ans1.status_code == 200
    assert ans1.json()["is_correct"] is True

    # Duplicate retry submission -> should return cached result without error or side-effects
    ans2 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "Hola"},
    )
    assert ans2.status_code == 200
    assert ans2.json()["is_correct"] is True
    assert ans2.json()["hearts_lost"] == 0


@pytest.mark.asyncio
async def test_duplicate_lesson_completion_idempotency(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    attempt_id = start_res.json()["attempt_id"]

    # Answer all exercises
    answers = [
        ("ex_gr1_1", "Hola"),
        ("ex_gr1_2", "Buenos días, ¿cómo estás?"),
        ("ex_gr1_3", "Buenos días, ¿cómo estás?"),
        ("ex_gr1_4", "días"),
        ("ex_gr1_5", "Adiós"),
        ("ex_gr1_6", "Good morning"),
    ]

    for ex_id, ans in answers:
        await client.post(
            f"/api/v1/lessons/lsn_greetings_1/exercises/{ex_id}/answer",
            json={"attempt_id": attempt_id, "answer": ans},
        )

    # First completion
    comp1 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert comp1.status_code == 200
    assert comp1.json()["already_completed"] is False

    # Second completion retry -> returns already_completed=True
    comp2 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert comp2.status_code == 200
    assert comp2.json()["already_completed"] is True
