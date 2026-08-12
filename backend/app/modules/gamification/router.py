from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.modules.gamification.repository import GamificationRepository
from app.modules.gamification.service import GamificationService
from app.modules.gamification.schemas import GamificationResponse

router = APIRouter(prefix="/gamification", tags=["gamification"])


def get_gamification_service(db: Session = Depends(get_db)) -> GamificationService:
    repository = GamificationRepository(db)
    return GamificationService(repository)


@router.get("/users/{user_id}", response_model=GamificationResponse)
def get_user_stats(user_id: str, service: GamificationService = Depends(get_gamification_service)):
    """Retrieve user gamification stats (XP, Hearts, Streak) (scaffolding)."""
    return service.get_user_stats(user_id)
