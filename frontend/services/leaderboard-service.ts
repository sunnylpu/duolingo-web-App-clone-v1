import { apiClient } from "@/lib/api-client";
import { LeaderboardResponse, LeaderboardPeriod, UserRankResponse } from "@/types";

export const leaderboardService = {
  getLeaderboard: (
    period: LeaderboardPeriod = "weekly",
    limit: number = 20,
    offset: number = 0
  ): Promise<LeaderboardResponse> =>
    apiClient.get<LeaderboardResponse>(
      `/leaderboard?period=${period}&limit=${limit}&offset=${offset}`
    ),

  getCurrentUserRank: (period: LeaderboardPeriod = "weekly"): Promise<UserRankResponse> =>
    apiClient.get<UserRankResponse>(`/leaderboard/me?period=${period}`),
};
