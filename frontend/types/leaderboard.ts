export type LeaderboardPeriod = "weekly" | "monthly" | "all_time";

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  username: string;
  display_name: string;
  avatar: string | null;
  xp: number;
  is_current_user: boolean;
}

export interface LeaderboardResponse {
  period: LeaderboardPeriod;
  entries: LeaderboardEntry[];
  current_user_rank: number | null;
  total_participants: number;
  limit: number;
  offset: number;
}

export interface UserRankResponse {
  period: LeaderboardPeriod;
  user_id: string;
  rank: number;
  xp: number;
  total_participants: number;
}
