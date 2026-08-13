import { apiClient } from "@/lib/api-client";
import { LessonAttempt } from "../types/lesson-session";

export interface AnswerSubmissionPayload {
  lessonId: string;
  exerciseId: string;
  attemptId: string | number;
  answer: string;
}

export interface AnswerSubmissionResult {
  exercise_id: string;
  is_correct: boolean;
  correct_answer: string;
  hearts_lost: number;
  hearts_remaining: number;
  attempt_completed: boolean;
}

export const lessonSessionService = {
  startLessonSession: (lessonId: string): Promise<LessonAttempt> =>
    apiClient.post<LessonAttempt>(`/lessons/${lessonId}/start`),

  submitAnswer: ({
    lessonId,
    exerciseId,
    attemptId,
    answer,
  }: AnswerSubmissionPayload): Promise<AnswerSubmissionResult> =>
    apiClient.post<AnswerSubmissionResult>(
      `/lessons/${lessonId}/exercises/${exerciseId}/answer`,
      {
        attempt_id: attemptId,
        answer,
      }
    ),
};
