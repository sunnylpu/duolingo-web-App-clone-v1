export interface LessonAttempt {
  attempt_id: string | number;
  lesson_id: string;
  status: "started" | "completed" | "failed" | "abandoned";
  started_at: string;
}

export type LessonSessionStep =
  | "intro"
  | "active_player"
  | "out_of_hearts"
  | "sequence_complete";
