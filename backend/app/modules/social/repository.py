import json
from typing import List, Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session, joinedload
from app.modules.social.models import UserFollowModel, ActivityEventModel
from app.modules.user.models import UserModel
from app.modules.gamification.models import UserStatsModel


class SocialRepository:
    """Handles data persistence for UserFollows and ActivityEvents."""

    def __init__(self, db: Session):
        self.db = db

    def is_following(self, follower_id: str, following_id: str) -> bool:
        return (
            self.db.query(UserFollowModel)
            .filter(
                UserFollowModel.follower_id == follower_id,
                UserFollowModel.following_id == following_id,
            )
            .first()
            is not None
        )

    def follow_user(self, follower_id: str, following_id: str) -> UserFollowModel:
        if follower_id == following_id:
            raise ValueError("Users cannot follow themselves.")

        existing = (
            self.db.query(UserFollowModel)
            .filter(
                UserFollowModel.follower_id == follower_id,
                UserFollowModel.following_id == following_id,
            )
            .first()
        )
        if existing:
            return existing

        follow_id = f"flw_{follower_id}_{following_id}"
        follow = UserFollowModel(
            id=follow_id,
            follower_id=follower_id,
            following_id=following_id,
        )
        self.db.add(follow)
        self.db.flush()
        return follow

    def unfollow_user(self, follower_id: str, following_id: str) -> bool:
        existing = (
            self.db.query(UserFollowModel)
            .filter(
                UserFollowModel.follower_id == follower_id,
                UserFollowModel.following_id == following_id,
            )
            .first()
        )
        if existing:
            self.db.delete(existing)
            self.db.flush()
            return True
        return False

    def get_following_ids(self, follower_id: str) -> List[str]:
        rows = (
            self.db.query(UserFollowModel.following_id)
            .filter(UserFollowModel.follower_id == follower_id)
            .all()
        )
        return [r.following_id for r in rows]

    def get_follower_ids(self, following_id: str) -> List[str]:
        rows = (
            self.db.query(UserFollowModel.follower_id)
            .filter(UserFollowModel.following_id == following_id)
            .all()
        )
        return [r.follower_id for r in rows]

    def get_followers_count(self, user_id: str) -> int:
        return (
            self.db.query(UserFollowModel)
            .filter(UserFollowModel.following_id == user_id)
            .count()
        )

    def get_following_count(self, user_id: str) -> int:
        return (
            self.db.query(UserFollowModel)
            .filter(UserFollowModel.follower_id == user_id)
            .count()
        )

    def record_activity(
        self,
        event_id: str,
        user_id: str,
        event_type: str,
        message: str,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ActivityEventModel:
        meta_str = json.dumps(metadata) if metadata else None
        event = ActivityEventModel(
            id=event_id,
            user_id=user_id,
            event_type=event_type,
            message=message,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata_json=meta_str,
        )
        self.db.add(event)
        self.db.flush()
        return event

    def get_activity_feed(
        self, user_ids: Optional[List[str]] = None, limit: int = 20, offset: int = 0
    ) -> Tuple[List[ActivityEventModel], int]:
        query = self.db.query(ActivityEventModel).options(joinedload(ActivityEventModel.user))
        if user_ids:
            query = query.filter(ActivityEventModel.user_id.in_(user_ids))

        total = query.count()
        items = (
            query.order_by(ActivityEventModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return items, total
