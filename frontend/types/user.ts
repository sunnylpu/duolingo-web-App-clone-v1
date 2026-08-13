export interface User {
  id: string;
  username: string;
  display_name: string;
  email: string;
  avatar: string | null;
  is_active: boolean;
}

export interface HeartRegenerationInfo {
  enabled?: boolean;
  seconds_until_next?: number | null;
  interval_seconds?: number;
}

export interface UserStats {
  total_xp: number;
  current_streak: number;
  longest_streak: number;
  hearts: number;
  max_hearts?: number;
  heart_regeneration?: HeartRegenerationInfo;
  gems: number;
  daily_goal_xp: number;
  daily_xp: number;
  daily_goal_completed?: boolean;
  activity_date?: string;
}

export interface LearningSummary {
  lessons_completed: number;
  skills_completed: number;
  skills_in_progress: number;
  course_progress_percent: number;
}

export interface UserProfile {
  user: User;
  stats: UserStats;
  learning: LearningSummary;
}
