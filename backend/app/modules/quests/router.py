from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.quests.service import QuestService
from app.modules.quests.schemas import (
    DailyQuestsResponse,
    WeeklyChallengeResponse,
    QuestHistoryResponse,
)

router = APIRouter(prefix="/quests", tags=["Quests"])


def get_quest_service(db: Session = Depends(get_db)) -> QuestService:
    return QuestService(db)


@router.get("/today", response_model=DailyQuestsResponse, summary="Get today's daily quests")
def get_today_quests(
    current_user: UserModel = Depends(get_current_user),
    service: QuestService = Depends(get_quest_service),
):
    """Return 3 assigned daily quests with real-time progress for current user."""
    return service.get_today_quests(current_user)


@router.get("/weekly", response_model=WeeklyChallengeResponse, summary="Get active weekly challenge")
def get_weekly_challenge(
    current_user: UserModel = Depends(get_current_user),
    service: QuestService = Depends(get_quest_service),
):
    """Return current week's active challenge and completion progress."""
    return service.get_weekly_challenge(current_user)


@router.get("/history", response_model=QuestHistoryResponse, summary="Get completed quest history")
def get_quest_history(
    limit: int = Query(20, ge=1, le=100),
    current_user: UserModel = Depends(get_current_user),
    service: QuestService = Depends(get_quest_service),
):
    """Return historical record of completed daily/weekly quests."""
    return service.get_quest_history(current_user, limit=limit)
