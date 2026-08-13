export interface LessonAttempt {
  attempt_id: number | string;
  lesson_id: string;
  status: "started" | "completed" | "failed" | "abandoned";
  started_at: string;
}

export type LessonSessionStep = "intro" | "active_player" | "sequence_complete";
