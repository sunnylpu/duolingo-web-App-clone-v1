import { apiClient } from "@/lib/api-client";
import { LessonAttempt } from "../types/lesson-session";

export const lessonSessionService = {
  startLessonSession: (lessonId: string): Promise<LessonAttempt> =>
    apiClient.post<LessonAttempt>(`/lessons/${lessonId}/start`),
};
