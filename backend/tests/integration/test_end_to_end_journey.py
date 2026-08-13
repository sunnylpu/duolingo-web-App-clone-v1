import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database


@pytest.fixture(autouse=True)
def setup_seed_data(db_session: Session):
    """Seed test database before integration test execution."""
    seed_database(db_session)


@pytest.mark.asyncio
async def test_full_end_to_end_learner_journey(client: AsyncClient):
    # 1. Fetch initial profile & stats
    profile_before = await client.get("/api/v1/users/me/profile")
    assert profile_before.status_code == 200
    xp_before = profile_before.json()["stats"]["total_xp"]

    # 2. Fetch learning path
    path_res = await client.get("/api/v1/path")
    assert path_res.status_code == 200
    path_data = path_res.json()
    assert path_data["recommended_skill_id"] is not None

    # 3. Start lesson lsn_greetings_1
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # 4. Answer exercise 1 incorrectly -> heart deducted
    ans1 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": "WrongAnswer"},
    )
    assert ans1.status_code == 200
    assert ans1.json()["is_correct"] is False
    assert ans1.json()["hearts_lost"] == 1

    # 5. Answer remaining exercises correctly
    answers = [
        ("ex_gr1_2", "Good morning"),
        ("ex_gr1_3", {"pairs": [["Hola", "Hello"], ["Gracias", "Thank you"], ["Adiós", "Goodbye"]]}),
        ("ex_gr1_4", "Buenas noches"),
        ("ex_gr1_5", "Hasta luego"),
        ("ex_gr1_6", "como"),
    ]

    for ex_id, ans in answers:
        res = await client.post(
            f"/api/v1/lessons/lsn_greetings_1/exercises/{ex_id}/answer",
            json={"attempt_id": attempt_id, "answer": ans},
        )
        assert res.status_code == 200
        assert res.json()["is_correct"] is True

    # 6. Complete lesson
    comp_res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/complete",
        json={"attempt_id": attempt_id},
    )
    assert comp_res.status_code == 200
    comp_data = comp_res.json()
    assert comp_data["status"] == "completed"
    assert comp_data["xp_earned"] > 0
    assert "streak" in comp_data
    assert "achievements" in comp_data

    # 7. Verify updated profile & leaderboard
    profile_after = await client.get("/api/v1/users/me/profile")
    assert profile_after.status_code == 200
    xp_after = profile_after.json()["stats"]["total_xp"]
    assert xp_after > xp_before

    lb_res = await client.get("/api/v1/leaderboard?period=weekly")
    assert lb_res.status_code == 200
    assert lb_res.json()["current_user_rank"] is not None
