from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.shared.database import get_db
from app.shared.security import get_current_user
from app.modules.user.models import UserModel
from app.modules.social.service import SocialService
from app.modules.social.schemas import (
    UserSocialSummary,
    SocialStatsResponse,
    ActivityFeedResponse,
    PublicProfileResponse,
    FriendSuggestionResponse,
)

router = APIRouter(prefix="/social", tags=["Social"])


def get_social_service(db: Session = Depends(get_db)) -> SocialService:
    return SocialService(db)


@router.post("/users/{user_id}/follow", summary="Follow a user")
def follow_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Establish a follow relationship with target user."""
    service.follow_user(current_user=current_user, target_user_id=user_id)
    return {"status": "following", "user_id": user_id}


@router.delete("/users/{user_id}/follow", summary="Unfollow a user")
def unfollow_user(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Remove follow relationship with target user."""
    service.unfollow_user(current_user=current_user, target_user_id=user_id)
    return {"status": "unfollowed", "user_id": user_id}


@router.get("/me", response_model=SocialStatsResponse, summary="Get current user social stats")
def get_my_social_stats(
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Return follower and following counts for current user."""
    return service.get_my_social_stats(current_user)


@router.get("/following", response_model=List[UserSocialSummary], summary="List users followed by current user")
def get_following(
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Return list of users followed by current user."""
    return service.get_following(current_user)


@router.get("/followers", response_model=List[UserSocialSummary], summary="List followers of current user")
def get_followers(
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Return list of followers of current user."""
    return service.get_followers(current_user)


@router.get("/suggestions", response_model=List[FriendSuggestionResponse], summary="Get friend suggestions")
def get_suggestions(
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Return list of recommended learners to follow."""
    return service.get_suggestions(current_user)


@router.get("/feed", response_model=ActivityFeedResponse, summary="Get social activity feed")
def get_activity_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Return chronological activity feed for user and followed friends."""
    return service.get_activity_feed(current_user=current_user, limit=limit, offset=offset)


@router.get("/users/{user_id}", response_model=PublicProfileResponse, summary="Get public learner profile")
def get_public_profile(
    user_id: str,
    current_user: UserModel = Depends(get_current_user),
    service: SocialService = Depends(get_social_service),
):
    """Return public stats, streaks, and follow status for target user."""
    return service.get_public_profile(current_user=current_user, target_user_id=user_id)
