export type ExerciseType =
  | "multiple_choice"
  | "translate"
  | "word_bank"
  | "match_pairs"
  | "fill_blank"
  | "type_answer";

export interface Exercise {
  id: string;
  type: ExerciseType;
  prompt: string;
  correct_answer: string;
  data: Record<string, any> | null;
  order: number;
  xp_reward: number;
}

export interface LessonDetail {
  id: string;
  skill_id: string;
  title: string;
  description: string | null;
  order_index: number;
  xp_reward: number;
  estimated_minutes: number;
  exercises: Exercise[];
}
