export interface User {
  id: string;
  username: string;
  display_name: string;
  email: string;
  avatar: string | null;
  is_active: boolean;
}

export interface UserStats {
  total_xp: number;
  current_streak: number;
  longest_streak: number;
  hearts: number;
  gems: number;
  daily_goal_xp: number;
  daily_xp: number;
  daily_goal_completed?: boolean;
  activity_date?: string;
}
