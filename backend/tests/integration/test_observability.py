"""
Integration tests for Phase 32 — Production Observability + Audit Trail + Operational Dashboard.

Verifies:
1. Request ID correlation and process timing middleware headers (X-Request-ID, X-Process-Time-MS)
2. Prometheus-compatible metrics endpoint (GET /metrics)
3. Health and readiness probes (GET /health/live, GET /health/ready)
4. Transactional audit trail logging (AuditEventModel & AuditService)
5. Ops overview telemetry endpoint (GET /api/v1/ops/overview)
"""

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app.main import app
from app.shared.audit import AuditService
from app.shared.audit_models import AuditEventModel
from app.shared.metrics import metrics_registry
from app.modules.user.models import UserModel
from seed.seed import seed_database

client = TestClient(app)


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_request_id_and_timing_headers():
    response = client.get("/health/live", headers={"X-Request-ID": "req_custom_123"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req_custom_123"
    assert "X-Process-Time-MS" in response.headers


def test_metrics_endpoint():
    metrics_registry.increment("lesson_completions_total", 5)

    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert "duolingo_lesson_completions_total" in response.text


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


def test_audit_service_recording(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()

    audit = AuditService.record_event(
        db=seeded_db,
        event_type="LESSON_COMPLETED",
        user_id=user_demo.id,
        entity_type="lesson",
        entity_id="lsn_greetings_01",
        metadata={"xp": 20},
        request_id="req_test_audit",
    )
    seeded_db.commit()

    saved = seeded_db.query(AuditEventModel).filter_by(id=audit.id).first()
    assert saved is not None
    assert saved.event_type == "LESSON_COMPLETED"
    assert saved.user_id == user_demo.id
    assert saved.request_id == "req_test_audit"


def test_ops_overview_endpoint():
    response = client.get("/api/v1/ops/overview")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert "system" in data
    assert data["system"]["database_status"] == "healthy"
