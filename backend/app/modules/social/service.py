import json
import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.modules.social.repository import SocialRepository
from app.modules.user.models import UserModel
from app.modules.gamification.models import UserStatsModel, UserAchievementModel
from app.modules.social.schemas import (
    UserSocialSummary,
    SocialStatsResponse,
    ActivityEventResponse,
    ActivityFeedResponse,
    PublicProfileResponse,
    FriendSuggestionResponse,
)
from app.shared.errors import NotFoundError, ValidationError


class SocialService:
    """Business logic for follow relationships, activity feeds, and friend suggestions."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = SocialRepository(db)

    def follow_user(self, current_user: UserModel, target_user_id: str) -> bool:
        if current_user.id == target_user_id:
            raise ValidationError("You cannot follow yourself.")

        target = self.db.query(UserModel).filter_by(id=target_user_id).first()
        if not target:
            raise NotFoundError(f"User '{target_user_id}' not found.")

        self.repository.follow_user(follower_id=current_user.id, following_id=target_user_id)
        self.db.commit()
        return True

    def unfollow_user(self, current_user: UserModel, target_user_id: str) -> bool:
        success = self.repository.unfollow_user(follower_id=current_user.id, following_id=target_user_id)
        self.db.commit()
        return success

    def get_my_social_stats(self, current_user: UserModel) -> SocialStatsResponse:
        followers = self.repository.get_followers_count(current_user.id)
        following = self.repository.get_following_count(current_user.id)
        return SocialStatsResponse(followers_count=followers, following_count=following)

    def get_following(self, current_user: UserModel) -> List[UserSocialSummary]:
        following_ids = self.repository.get_following_ids(current_user.id)
        users = self.db.query(UserModel).filter(UserModel.id.in_(following_ids)).all() if following_ids else []

        results: List[UserSocialSummary] = []
        for u in users:
            stats = self.db.query(UserStatsModel).filter_by(user_id=u.id).first()
            results.append(
                UserSocialSummary(
                    id=u.id,
                    username=u.username,
                    display_name=u.display_name,
                    avatar=u.avatar,
                    total_xp=stats.total_xp if stats else 0,
                    current_streak=stats.current_streak if stats else 0,
                    is_following=True,
                )
            )
        return results

    def get_followers(self, current_user: UserModel) -> List[UserSocialSummary]:
        follower_ids = self.repository.get_follower_ids(current_user.id)
        users = self.db.query(UserModel).filter(UserModel.id.in_(follower_ids)).all() if follower_ids else []

        results: List[UserSocialSummary] = []
        for u in users:
            stats = self.db.query(UserStatsModel).filter_by(user_id=u.id).first()
            is_flw = self.repository.is_following(current_user.id, u.id)
            results.append(
                UserSocialSummary(
                    id=u.id,
                    username=u.username,
                    display_name=u.display_name,
                    avatar=u.avatar,
                    total_xp=stats.total_xp if stats else 0,
                    current_streak=stats.current_streak if stats else 0,
                    is_following=is_flw,
                )
            )
        return results

    def get_suggestions(self, current_user: UserModel) -> List[FriendSuggestionResponse]:
        following_ids = set(self.repository.get_following_ids(current_user.id))
        following_ids.add(current_user.id)

        candidates = (
            self.db.query(UserModel)
            .filter(UserModel.id.not_in(following_ids))
            .limit(10)
            .all()
        )

        results: List[FriendSuggestionResponse] = []
        for cand in candidates:
            stats = self.db.query(UserStatsModel).filter_by(user_id=cand.id).first()
            results.append(
                FriendSuggestionResponse(
                    user=UserSocialSummary(
                        id=cand.id,
                        username=cand.username,
                        display_name=cand.display_name,
                        avatar=cand.avatar,
                        total_xp=stats.total_xp if stats else 0,
                        current_streak=stats.current_streak if stats else 0,
                        is_following=False,
                    ),
                    reason="Leaderboard contender",
                )
            )
        return results

    def get_activity_feed(
        self, current_user: UserModel, limit: int = 20, offset: int = 0
    ) -> ActivityFeedResponse:
        following_ids = self.repository.get_following_ids(current_user.id)
        relevant_user_ids = [current_user.id] + following_ids

        events, total = self.repository.get_activity_feed(
            user_ids=relevant_user_ids, limit=limit, offset=offset
        )

        items: List[ActivityEventResponse] = []
        for ev in events:
            u = ev.user
            u_stats = self.db.query(UserStatsModel).filter_by(user_id=u.id).first() if u else None
            meta_dict = json.loads(ev.metadata_json) if ev.metadata_json else None

            user_summary = UserSocialSummary(
                id=u.id if u else "usr_unknown",
                username=u.username if u else "unknown",
                display_name=u.display_name if u else "Learner",
                avatar=u.avatar if u else "⚡",
                total_xp=u_stats.total_xp if u_stats else 0,
                current_streak=u_stats.current_streak if u_stats else 0,
                is_following=self.repository.is_following(current_user.id, u.id) if u else False,
            )

            items.append(
                ActivityEventResponse(
                    id=ev.id,
                    user=user_summary,
                    event_type=ev.event_type,
                    message=ev.message,
                    metadata=meta_dict,
                    created_at=ev.created_at,
                )
            )

        return ActivityFeedResponse(items=items, total=total)

    def get_public_profile(
        self, current_user: UserModel, target_user_id: str
    ) -> PublicProfileResponse:
        user = self.db.query(UserModel).filter_by(id=target_user_id).first()
        if not user:
            raise NotFoundError(f"Learner '{target_user_id}' not found.")

        stats = self.db.query(UserStatsModel).filter_by(user_id=user.id).first()
        followers = self.repository.get_followers_count(user.id)
        following = self.repository.get_following_count(user.id)
        is_flw = self.repository.is_following(current_user.id, user.id)

        return PublicProfileResponse(
            id=user.id,
            username=user.username,
            display_name=user.display_name,
            avatar=user.avatar,
            total_xp=stats.total_xp if stats else 0,
            current_streak=stats.current_streak if stats else 0,
            longest_streak=stats.longest_streak if stats else 0,
            followers_count=followers,
            following_count=following,
            is_following=is_flw,
        )

    def record_activity_event(
        self,
        user_id: str,
        event_type: str,
        message: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        ev_id = f"act_{uuid.uuid4().hex[:12]}"
        self.repository.record_activity(
            event_id=ev_id,
            user_id=user_id,
            event_type=event_type,
            message=message,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata=metadata,
        )
        self.db.commit()
