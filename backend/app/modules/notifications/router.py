from typing import Optional
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.notifications.service import NotificationService
from app.modules.notifications.schemas import (
    NotificationListResponse,
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=NotificationListResponse)
def get_user_notifications(
    unread_only: bool = Query(False, description="Filter for unread notifications only"),
    limit: int = Query(20, ge=1, le=100, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve chronologically ordered notifications for current user with unread metadata."""
    svc = NotificationService(db)
    return svc.get_user_notifications(
        current_user=current_user, unread_only=unread_only, limit=limit, offset=offset
    )


@router.post("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: str = Path(..., description="Unique notification ID"),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark a specific notification as read. Enforces strict user ownership."""
    svc = NotificationService(db)
    svc.mark_as_read(current_user=current_user, notification_id=notification_id)
    return {"status": "success", "message": "Notification marked as read"}


@router.post("/read-all")
def mark_all_notifications_as_read(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Mark all notifications for the current user as read."""
    svc = NotificationService(db)
    count = svc.mark_all_as_read(current_user=current_user)
    return {"status": "success", "marked_read_count": count}


@router.get("/preferences", response_model=NotificationPreferenceResponse)
def get_notification_preferences(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieve notification delivery category preferences for current user."""
    svc = NotificationService(db)
    return svc.get_preferences(current_user=current_user)


@router.patch("/preferences", response_model=NotificationPreferenceResponse)
def update_notification_preferences(
    payload: NotificationPreferenceUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update notification category toggle preferences for current user."""
    svc = NotificationService(db)
    return svc.update_preferences(current_user=current_user, payload=payload)
