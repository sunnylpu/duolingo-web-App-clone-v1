from typing import List, Optional, Dict, Any
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.leaderboard.repository import LeaderboardRepository
from app.modules.social.repository import SocialRepository
from app.modules.user.models import UserModel
from app.modules.gamification.models import UserStatsModel
from app.modules.progress.models import DailyActivityModel
from app.modules.gamification.service import get_current_activity_date
from app.modules.leaderboard.schemas import (
    LeaderboardResponse,
    LeaderboardEntryResponse,
    UserRankResponse,
)
from app.shared.errors import ValidationError, NotFoundError


class LeaderboardService:
    """Contains business logic for Leaderboard rankings, period standings, and competition ranking."""

    VALID_PERIODS = {"weekly", "monthly", "all_time"}

    def __init__(self, db: Session):
        self.db = db
        self.repository = LeaderboardRepository(db)
        self.social_repository = SocialRepository(db)

    def _calculate_ranked_entries(
        self, period: str, current_user_id: Optional[str] = None, scope: str = "global"
    ) -> List[Dict[str, Any]]:
        today = get_current_activity_date()

        user_query = self.db.query(UserModel)
        if scope == "friends" and current_user_id:
            following_ids = self.social_repository.get_following_ids(current_user_id)
            friend_user_ids = set(following_ids + [current_user_id])
            user_query = user_query.filter(UserModel.id.in_(friend_user_ids))

        all_users = user_query.all()
        user_map = {u.id: u for u in all_users}

        xp_map: Dict[str, int] = {}

        if period == "all_time":
            all_stats = self.db.query(UserStatsModel).filter(
                UserStatsModel.user_id.in_(user_map.keys()) if user_map else True
            ).all()
            for st in all_stats:
                xp_map[st.user_id] = st.total_xp
            for u_id in user_map:
                if u_id not in xp_map:
                    xp_map[u_id] = 0
        else:
            if period == "weekly":
                start_date = today - timedelta(days=today.weekday())
            else:  # monthly
                start_date = today.replace(day=1)

            activity_sums = (
                self.db.query(
                    DailyActivityModel.user_id,
                    func.sum(DailyActivityModel.xp_earned).label("period_xp"),
                )
                .filter(
                    DailyActivityModel.activity_date >= start_date,
                    DailyActivityModel.user_id.in_(user_map.keys()) if user_map else True,
                )
                .group_by(DailyActivityModel.user_id)
                .all()
            )

            for u_id, period_xp in activity_sums:
                xp_map[u_id] = int(period_xp or 0)

            for u_id in user_map:
                if u_id not in xp_map:
                    xp_map[u_id] = 0

        sorted_user_ids = sorted(
            xp_map.keys(),
            key=lambda uid: (
                -xp_map[uid],
                (user_map[uid].display_name if uid in user_map else "").lower(),
            ),
        )

        ranked_list: List[Dict[str, Any]] = []
        prev_xp: Optional[int] = None

        for idx, u_id in enumerate(sorted_user_ids):
            user_xp = xp_map[u_id]
            if prev_xp is not None and user_xp == prev_xp:
                rank = ranked_list[-1]["rank"]
            else:
                rank = idx + 1

            prev_xp = user_xp
            user_obj = user_map.get(u_id)

            ranked_list.append(
                {
                    "rank": rank,
                    "user_id": u_id,
                    "username": user_obj.username if user_obj else "unknown",
                    "display_name": user_obj.display_name if user_obj else "Unknown Learner",
                    "avatar": user_obj.avatar if user_obj else None,
                    "xp": user_xp,
                    "is_current_user": (u_id == current_user_id),
                }
            )

        return ranked_list

    def get_leaderboard(
        self,
        period: str = "weekly",
        scope: str = "global",
        limit: int = 20,
        offset: int = 0,
        current_user_id: Optional[str] = None,
    ) -> LeaderboardResponse:
        period_clean = period.lower().strip() if period else "weekly"
        if period_clean not in self.VALID_PERIODS:
            raise ValidationError(
                f"Invalid period parameter '{period}'. Allowed values: {', '.join(sorted(self.VALID_PERIODS))}."
            )

        limit_clean = max(1, min(100, limit))
        offset_clean = max(0, offset)

        ranked_all = self._calculate_ranked_entries(
            period=period_clean, current_user_id=current_user_id, scope=scope.lower()
        )
        total_participants = len(ranked_all)

        current_user_rank = None
        if current_user_id:
            for item in ranked_all:
                if item["user_id"] == current_user_id:
                    current_user_rank = item["rank"]
                    break

        sliced = ranked_all[offset_clean : offset_clean + limit_clean]
        entries = [LeaderboardEntryResponse(**item) for item in sliced]

        return LeaderboardResponse(
            period=period_clean,
            entries=entries,
            current_user_rank=current_user_rank,
            total_participants=total_participants,
            limit=limit_clean,
            offset=offset_clean,
        )

    def get_current_user_rank(self, user_id: str, period: str = "weekly") -> UserRankResponse:
        period_clean = period.lower().strip() if period else "weekly"
        if period_clean not in self.VALID_PERIODS:
            raise ValidationError(
                f"Invalid period parameter '{period}'. Allowed values: {', '.join(sorted(self.VALID_PERIODS))}."
            )

        ranked_all = self._calculate_ranked_entries(period_clean, current_user_id=user_id)
        for item in ranked_all:
            if item["user_id"] == user_id:
                return UserRankResponse(
                    period=period_clean,
                    user_id=user_id,
                    rank=item["rank"],
                    xp=item["xp"],
                    total_participants=len(ranked_all),
                )

        raise NotFoundError(f"User '{user_id}' rank not found for period '{period_clean}'.")
