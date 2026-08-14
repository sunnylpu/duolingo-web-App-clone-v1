"""
Integration & Security Tests for Phase 35 & 36 — Production Authentication + Authorization + Hardened Sessions.

Verifies:
1. User registration flow with password hashing & HttpOnly cookie (no raw token in response)
2. Login credential verification & HttpOnly cookie session management
3. Programmatic token endpoint (/auth/token)
4. Current user session profile retrieval
5. Admin role authorization enforcement (require_admin dependency)
6. True session revocation on logout
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.shared.database import get_db
from app.shared.security import token_blocklist
from app.shared.rate_limit import rate_limiter
from seed.seed import seed_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_seeded_database(db_session: Session):
    token_blocklist.clear()
    rate_limiter.clear()
    client.cookies.clear()
    seed_database(db_session)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield db_session
    app.dependency_overrides.clear()
    token_blocklist.clear()
    rate_limiter.clear()
    client.cookies.clear()


def test_user_registration_success():
    uid = uuid.uuid4().hex[:6]
    payload = {
        "email": f"auth_learner_{uid}@example.com",
        "username": f"auth_{uid}",
        "password": "SecurePassword123!",
        "display_name": "Auth Learner",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Browser response does NOT leak raw JWT token in JSON body
    assert "access_token" not in data
    assert data["status"] == "authenticated"
    assert data["user"]["email"] == payload["email"]
    assert data["user"]["username"] == payload["username"]
    assert "auth_token" in response.cookies


def test_duplicate_user_registration_rejection():
    payload = {
        "email": "demo@duolingo.clone",
        "username": "demolearner",
        "password": "SecurePassword123!",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] in ["DUPLICATE_EMAIL", "DUPLICATE_USERNAME", "VALIDATION_ERROR"]


def test_login_success_with_cookie_session():
    login_payload = {
        "email_or_username": "demolearner",
        "password": "demopassword123",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()

    # Token is stored safely in HttpOnly cookie, not JSON body
    assert "access_token" not in data
    assert data["status"] == "authenticated"
    assert data["user"]["username"] == "demolearner"
    assert "auth_token" in response.cookies


def test_programmatic_api_token_endpoint():
    token_payload = {
        "email_or_username": "demolearner",
        "password": "demopassword123",
    }
    response = client.post("/api/v1/auth/token", json=token_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in_minutes"] > 0


def test_invalid_login_credentials_rejection():
    bad_payload = {
        "email_or_username": "demolearner",
        "password": "WrongPassword123!",
    }
    response = client.post("/api/v1/auth/login", json=bad_payload)
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "INVALID_CREDENTIALS"


def test_get_current_user_me_endpoint():
    token_res = client.post(
        "/api/v1/auth/token",
        json={"email_or_username": "demolearner", "password": "demopassword123"},
    )
    token = token_res.json()["access_token"]

    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "demolearner"


def test_admin_role_authorization_enforcement():
    # 1. Standard user token
    user_token_res = client.post(
        "/api/v1/auth/token",
        json={"email_or_username": "demolearner", "password": "demopassword123"},
    )
    user_token = user_token_res.json()["access_token"]

    # Standard user attempting admin endpoint -> 403 Forbidden
    forbidden_res = client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert forbidden_res.status_code == 403
    assert forbidden_res.json()["error"]["code"] == "FORBIDDEN"

    # 2. Admin user token
    admin_token_res = client.post(
        "/api/v1/auth/token",
        json={"email_or_username": "admin", "password": "adminpassword123"},
    )
    admin_token = admin_token_res.json()["access_token"]

    # Admin user accessing admin overview -> 200 OK
    admin_res = client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert admin_res.status_code == 200
    assert "users" in admin_res.json()
    assert "system" in admin_res.json()


def test_logout_session_revocation():
    token_res = client.post(
        "/api/v1/auth/token",
        json={"email_or_username": "demolearner", "password": "demopassword123"},
    )
    token = token_res.json()["access_token"]

    # Verify token works initially
    me_before = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_before.status_code == 200

    # Logout and revoke token
    logout_res = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_res.status_code == 200
    assert logout_res.json()["status"] == "ok"

    # Verify revoked token is rejected
    me_after = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_after.status_code == 401
    assert me_after.json()["error"]["code"] == "SESSION_REVOKED"
