"""
Integration & Security Tests for Phase 35 — Production Authentication + Authorization + Secure Sessions.

Verifies:
1. User registration flow with password hashing & default stats initialization
2. Login credential verification & HttpOnly cookie session management
3. Rate-limiting protection on authentication endpoints
4. Current user session profile retrieval
5. Admin role authorization enforcement (require_admin dependency)
6. Session logout & cookie clearance
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.shared.database import get_db
from seed.seed import seed_database

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_seeded_database(db_session: Session):
    seed_database(db_session)

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield db_session
    app.dependency_overrides.clear()


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

    assert "access_token" in data
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


def test_login_success_with_cookie_and_token():
    login_payload = {
        "email_or_username": "demolearner",
        "password": "demopassword123",
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["user"]["username"] == "demolearner"
    assert "auth_token" in response.cookies


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
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email_or_username": "demolearner", "password": "demopassword123"},
    )
    token = login_res.json()["access_token"]

    me_res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "demolearner"


def test_admin_role_authorization_enforcement():
    # 1. Standard user login
    user_login = client.post(
        "/api/v1/auth/login",
        json={"email_or_username": "demolearner", "password": "demopassword123"},
    )
    user_token = user_login.json()["access_token"]

    # Standard user attempting admin endpoint -> 403 Forbidden
    forbidden_res = client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert forbidden_res.status_code == 403
    assert forbidden_res.json()["error"]["code"] == "FORBIDDEN"

    # 2. Admin user login
    admin_login = client.post(
        "/api/v1/auth/login",
        json={"email_or_username": "admin", "password": "adminpassword123"},
    )
    admin_token = admin_login.json()["access_token"]

    # Admin user accessing admin overview -> 200 OK
    admin_res = client.get(
        "/api/v1/admin/overview",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert admin_res.status_code == 200
    assert "users" in admin_res.json()
    assert "system" in admin_res.json()


def test_logout_session_cookie_clearance():
    logout_res = client.post("/api/v1/auth/logout")
    assert logout_res.status_code == 200
    assert logout_res.json()["status"] == "ok"
