export interface GamificationStats {
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

export interface DailyActivity {
  date: string;
  xp_earned: number;
  lessons_completed: number;
  goal_xp: number;
  goal_completed: boolean;
}
