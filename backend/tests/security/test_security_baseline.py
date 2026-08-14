"""
Security baseline tests — verifies that auth-protected endpoints behave correctly,
injection payloads are rejected, and security headers are present.

Updated for Phase 36: all lesson API calls require authentication.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from seed.seed import seed_database
from app.modules.gamification.service import GamificationService
from app.shared.security import create_access_token


@pytest.fixture(autouse=True)
def setup_seed_data(db_session: Session):
    """Seed test database before security baseline test execution."""
    seed_database(db_session)


@pytest.mark.asyncio
async def test_security_headers_present(client: AsyncClient):
    res = await client.get("/health")
    assert res.status_code == 200
    headers = res.headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "DENY"
    assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert headers.get("X-XSS-Protection") == "1; mode=block"


@pytest.mark.asyncio
async def test_server_side_authorization_locked_lesson_rejection(client: AsyncClient):
    # Attempting to start locked lesson lsn_food_1 -> HTTP 409 SKILL_LOCKED
    # client already carries usr_demo Bearer token (from conftest)
    res = await client.post("/api/v1/lessons/lsn_food_1/start")
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "SKILL_LOCKED"


@pytest.mark.asyncio
async def test_input_validation_malformed_answer_rejection(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    # Invalid exercise ID -> HTTP 404
    res_404 = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/invalid_ex_id/answer",
        json={"attempt_id": attempt_id, "answer": "test"},
    )
    assert res_404.status_code == 404

    # Invalid attempt ID -> HTTP 404
    res_invalid_att = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": 999999, "answer": "test"},
    )
    assert res_invalid_att.status_code == 404


@pytest.mark.asyncio
async def test_sql_injection_payload_resilience(client: AsyncClient):
    # Pass SQL injection strings in parameters & path variables
    sql_payload = "lsn_greetings_1' OR '1'='1"
    res = await client.get(f"/api/v1/lessons/{sql_payload}")
    assert res.status_code == 404

    res2 = await client.get("/api/v1/leaderboard?period=weekly' OR '1'='1")
    assert res2.status_code in (400, 422)  # Safely rejected by validation layer without SQL execution


@pytest.mark.asyncio
async def test_xss_script_string_safety(client: AsyncClient):
    start_res = await client.post("/api/v1/lessons/lsn_greetings_1/start")
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    xss_payload = "<script>alert('XSS')</script>"
    res = await client.post(
        "/api/v1/lessons/lsn_greetings_1/exercises/ex_gr1_1/answer",
        json={"attempt_id": attempt_id, "answer": xss_payload},
    )
    assert res.status_code == 200
    assert res.json()["is_correct"] is False
