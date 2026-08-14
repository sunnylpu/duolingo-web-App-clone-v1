"""
Integration tests for Phase 32 — Production Observability, Audit Trail & Metrics.

Verifies:
1. X-Request-ID and X-Process-Time-MS header injection
2. Prometheus /metrics endpoint format and counters
3. Health /health/live and /health/ready probes
4. AuditService transactional logging
5. Ops overview telemetry endpoint response schema with admin protection
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.shared.database import get_db
from app.shared.audit import AuditService
from app.shared.audit_models import AuditEventModel
from app.modules.user.models import UserModel
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


def test_request_id_and_timing_headers():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"].startswith("req_")
    assert "X-Process-Time-MS" in response.headers


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    content = response.text
    assert "duolingo_requests_total" in content
    assert "duolingo_lesson_completions_total" in content


def test_health_and_readiness_probes():
    # Test Live
    res_live = client.get("/health/live")
    assert res_live.status_code == 200
    assert res_live.json()["status"] == "ok"
    assert "version" in res_live.json()

    # Test Ready
    res_ready = client.get("/health/ready")
    assert res_ready.status_code == 200
    assert res_ready.json()["status"] == "ready"
    assert res_ready.json()["checks"]["database"] == "ok"


def test_audit_service_recording(db_session: Session):
    user_demo = db_session.query(UserModel).filter_by(id="usr_demo").first()

    audit = AuditService.record_event(
        db=db_session,
        event_type="LESSON_COMPLETED",
        user_id=user_demo.id,
        entity_type="lesson",
        entity_id="lsn_greetings_01",
        metadata={"xp": 20},
        request_id="req_test_audit",
    )
    db_session.commit()

    saved = db_session.query(AuditEventModel).filter_by(id=audit.id).first()
    assert saved is not None
    assert saved.event_type == "LESSON_COMPLETED"
    assert saved.user_id == user_demo.id
    assert saved.request_id == "req_test_audit"


def test_ops_overview_endpoint():
    from app.shared.security import create_access_token
    admin_token = create_access_token("usr_admin", role="admin")
    response = client.get(
        "/api/v1/ops/overview",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "system" in data
    assert data["system"]["database_status"] == "healthy"
