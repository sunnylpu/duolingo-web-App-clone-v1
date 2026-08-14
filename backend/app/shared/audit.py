import json
import uuid
import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.shared.audit_models import AuditEventModel


class AuditService:
    """Transactional operational audit logger for tracking business-critical domain events."""

    @staticmethod
    def record_event(
        db: Session,
        event_type: str,
        user_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> AuditEventModel:
        audit_id = f"aud_{uuid.uuid4().hex[:12]}"
        meta_str = json.dumps(metadata) if metadata else None

        event = AuditEventModel(
            id=audit_id,
            user_id=user_id,
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata_json=meta_str,
            request_id=request_id,
            created_at=datetime.datetime.utcnow(),
        )
        db.add(event)
        db.flush()
        return event
