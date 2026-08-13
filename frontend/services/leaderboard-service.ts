import { apiClient } from "@/lib/api-client";
import { LeaderboardResponse, LeaderboardPeriod } from "@/types";

export const leaderboardService = {
  getLeaderboard: (period: LeaderboardPeriod = "weekly"): Promise<LeaderboardResponse> =>
    apiClient.get<LeaderboardResponse>(`/leaderboard?period=${encodeURIComponent(period)}`),
};
