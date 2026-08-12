from app.modules.leaderboard.repository import LeaderboardRepository
from app.modules.leaderboard.schemas import LeaderboardResponse, LeaderboardEntry


class LeaderboardService:
    """Contains business logic for Leaderboard leagues and rankings."""

    def __init__(self, repository: LeaderboardRepository):
        self.repository = repository

    def get_leaderboard(self, league_name: str = "Bronze") -> LeaderboardResponse:
        return LeaderboardResponse(
            league_name=league_name,
            entries=[
                LeaderboardEntry(user_id="usr_01", username="learner1", weekly_xp=150, rank=1),
                LeaderboardEntry(user_id="usr_02", username="polyglot", weekly_xp=120, rank=2),
            ],
        )
