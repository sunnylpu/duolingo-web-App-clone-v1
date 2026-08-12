export interface User {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
}

export interface Course {
  id: string;
  title: string;
  source_language: string;
  target_language: string;
}

export interface Lesson {
  id: string;
  title: string;
  order: number;
  unit_id: string;
}

export interface GamificationStats {
  id: string;
  user_id: string;
  xp: number;
  streak_count: number;
  hearts: number;
  gems: number;
}
