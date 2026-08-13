export interface Achievement {
  id: string;
  code: string;
  name: string;
  description: string;
  icon: string;
  requirement_type: string;
  requirement_value: number;
}

export interface UserAchievement {
  achievement: Achievement;
  is_earned: boolean;
  earned_at: string | null;
  progress?: number;
  target?: number;
}
