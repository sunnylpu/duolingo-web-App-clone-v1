"""
Phase 36.1 — JWT Claims Hardening, CSRF Origin Tightening & Revocation Tests.

Verifies:
1. JWT tokens contain jti, iss, aud, sub, role, exp, iat claims
2. Tokens with forged/missing issuer are rejected
3. Tokens with forged/missing audience are rejected
4. Revoked jti is rejected on subsequent requests
5. Malicious origin (prefix bypass, subdomain bypass) is rejected by CSRF middleware
6. Trusted origin is accepted
7. Production config fails fast with dev auth bypass enabled
8. Dev auth bypass is never reachable in production config
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import jwt as pyjwt

from app.main import app
from app.config import Settings, settings
from app.shared.database import get_db
from app.shared.security import create_access_token, token_blocklist, decode_access_token
from app.shared.rate_limit import rate_limiter
from app.modules.lesson.models import LessonModel, ExerciseModel
from app.modules.notifications.models import NotificationModel
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


# ---------------------------------------------------------------------------
# 1. JWT claim structure
# ---------------------------------------------------------------------------

def test_jwt_contains_required_owasp_claims():
    """Every token must include jti, iss, aud, sub, role, exp, iat."""
    token = create_access_token("usr_demo", role="user")
    payload = pyjwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=["HS256"],
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER,
    )
    assert "jti" in payload, "jti (unique token ID) is missing from JWT"
    assert "iss" in payload, "iss (issuer) is missing from JWT"
    assert "aud" in payload, "aud (audience) is missing from JWT"
    assert "sub" in payload
    assert "role" in payload
    assert "exp" in payload
    assert "iat" in payload
    assert payload["iss"] == settings.JWT_ISSUER
    assert payload["aud"] == settings.JWT_AUDIENCE
    assert payload["sub"] == "usr_demo"
    assert payload["role"] == "user"


def test_each_token_has_unique_jti():
    """Two tokens for the same user must have different jti values."""
    t1 = create_access_token("usr_demo")
    t2 = create_access_token("usr_demo")
    p1 = pyjwt.decode(t1, settings.JWT_SECRET_KEY, algorithms=["HS256"],
                      audience=settings.JWT_AUDIENCE, issuer=settings.JWT_ISSUER)
    p2 = pyjwt.decode(t2, settings.JWT_SECRET_KEY, algorithms=["HS256"],
                      audience=settings.JWT_AUDIENCE, issuer=settings.JWT_ISSUER)
    assert p1["jti"] != p2["jti"], "jti must be unique per token"


# ---------------------------------------------------------------------------
# 2. Forged issuer / audience rejection
# ---------------------------------------------------------------------------

def test_token_with_forged_issuer_is_rejected():
    """A token signed with the correct secret but a wrong issuer must be rejected."""
    import datetime
    forged_payload = {
        "sub": "usr_demo",
        "role": "user",
        "jti": str(uuid.uuid4()),
        "iss": "evil-attacker-service",      # forged issuer
        "aud": settings.JWT_AUDIENCE,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    forged_token = pyjwt.encode(forged_payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    res = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {forged_token}"},
    )
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_token_with_forged_audience_is_rejected():
    """A token signed with the correct secret but a wrong audience must be rejected."""
    import datetime
    forged_payload = {
        "sub": "usr_demo",
        "role": "user",
        "jti": str(uuid.uuid4()),
        "iss": settings.JWT_ISSUER,
        "aud": "evil-third-party-app",       # forged audience
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    forged_token = pyjwt.encode(forged_payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    res = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {forged_token}"},
    )
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_token_without_iss_aud_is_rejected():
    """A legacy token without iss/aud claims (pre-36.1) must be rejected."""
    import datetime
    legacy_payload = {
        "sub": "usr_demo",
        "role": "user",
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    legacy_token = pyjwt.encode(legacy_payload, settings.JWT_SECRET_KEY, algorithm="HS256")

    res = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {legacy_token}"},
    )
    assert res.status_code == 401


# ---------------------------------------------------------------------------
# 3. jti-based revocation
# ---------------------------------------------------------------------------

def test_revoked_jti_rejects_subsequent_requests():
    """After logout, the jti must be in the blocklist and any subsequent request must be rejected."""
    token = create_access_token("usr_demo", role="user")
    payload = decode_access_token(token)
    jti = payload["jti"]
    exp = payload["exp"]

    # Revoke the jti directly
    token_blocklist.revoke_jti(jti, exp)

    res = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "SESSION_REVOKED"


def test_logout_revokes_jti_and_blocks_reuse():
    """Logout endpoint must revoke the jti; the same token must be rejected afterwards."""
    token = create_access_token("usr_demo", role="user")

    # Confirm token works before logout
    before = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert before.status_code == 200

    # Logout via Bearer header
    logout = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout.status_code == 200

    # Same token must now be rejected
    after = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token}"})
    assert after.status_code == 401
    assert after.json()["error"]["code"] == "SESSION_REVOKED"


def test_different_tokens_independent_revocation():
    """Revoking one token must not affect a second independently-issued token."""
    token_a = create_access_token("usr_demo", role="user")
    token_b = create_access_token("usr_demo", role="user")

    # Revoke token_a only
    payload_a = decode_access_token(token_a)
    token_blocklist.revoke_jti(payload_a["jti"], payload_a["exp"])

    # token_a must be rejected
    res_a = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token_a}"})
    assert res_a.status_code == 401

    # token_b must still be accepted
    res_b = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {token_b}"})
    assert res_b.status_code == 200


# ---------------------------------------------------------------------------
# 4. CSRF origin tightening
# ---------------------------------------------------------------------------

def test_csrf_rejects_evil_prefix_origin():
    """
    Prefix-match bypass: https://localhost:3000.evil.com must be rejected
    even though it starts with the allowed 'http://localhost:3000'.
    """
    token = create_access_token("usr_demo", role="user")
    res = client.post(
        "/api/v1/gamification/hearts/refill",
        cookies={"auth_token": token},
        headers={
            "Origin": "http://localhost:3000.evil.com",
        },
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "CSRF_REJECTED"


def test_csrf_rejects_subdomain_origin():
    """
    Subdomain bypass: https://evil.localhost:3000 must be rejected even though
    the domain contains the allowed hostname as a suffix.
    """
    token = create_access_token("usr_demo", role="user")
    res = client.post(
        "/api/v1/gamification/hearts/refill",
        cookies={"auth_token": token},
        headers={
            "Origin": "http://evil.localhost:3000",
        },
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "CSRF_REJECTED"


def test_csrf_rejects_cross_origin_referer():
    """
    Cross-origin Referer: a request with a Referer pointing to an untrusted host
    and no X-Requested-With must be rejected.
    """
    token = create_access_token("usr_demo", role="user")
    res = client.post(
        "/api/v1/gamification/hearts/refill",
        cookies={"auth_token": token},
        headers={
            "Referer": "https://attacker-site.example.com/csrf.html",
        },
    )
    assert res.status_code == 403
    assert res.json()["error"]["code"] == "CSRF_REJECTED"


def test_csrf_accepts_trusted_origin():
    """An exact match on the allowed CORS origin must be accepted."""
    token = create_access_token("usr_demo", role="user")
    res = client.post(
        "/api/v1/gamification/hearts/refill",
        cookies={"auth_token": token},
        headers={
            "Origin": "http://localhost:3000",
        },
    )
    assert res.status_code == 200


def test_csrf_accepts_x_requested_with_header():
    """X-Requested-With: XMLHttpRequest is always a safe AJAX indicator."""
    token = create_access_token("usr_demo", role="user")
    res = client.post(
        "/api/v1/gamification/hearts/refill",
        cookies={"auth_token": token},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    assert res.status_code == 200


# ---------------------------------------------------------------------------
# 5. Production config hardening (dev bypass)
# ---------------------------------------------------------------------------

def test_production_config_rejects_dev_auth_bypass():
    """ALLOW_DEV_AUTH_BYPASS=True must raise ValueError in production mode."""
    with pytest.raises(ValueError, match="ALLOW_DEV_AUTH_BYPASS"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            JWT_SECRET_KEY="a" * 32,
            ALLOW_DEV_AUTH_BYPASS=True,
        )


def test_production_config_fails_on_weak_jwt_secret():
    """Short or default JWT_SECRET_KEY must raise ValueError in production."""
    with pytest.raises(ValueError, match="strong, non-default JWT_SECRET_KEY"):
        Settings(
            APP_ENV="production",
            DEBUG=False,
            JWT_SECRET_KEY="too_short",
        )


def test_production_config_fails_on_debug_mode():
    """DEBUG=True must raise ValueError in production."""
    with pytest.raises(ValueError, match="DEBUG mode must be disabled"):
        Settings(
            APP_ENV="production",
            DEBUG=True,
            JWT_SECRET_KEY="a" * 32,
        )


def test_valid_production_config_passes():
    """A fully correct production config must not raise any errors."""
    s = Settings(
        APP_ENV="production",
        DEBUG=False,
        JWT_SECRET_KEY="a_very_long_and_strong_secret_key_for_production_use",
        ALLOW_DEV_AUTH_BYPASS=False,
    )
    assert s.APP_ENV == "production"
    assert s.DEBUG is False
    assert s.ALLOW_DEV_AUTH_BYPASS is False
