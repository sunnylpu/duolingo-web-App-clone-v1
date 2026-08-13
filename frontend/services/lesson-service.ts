import { apiClient } from "@/lib/api-client";
import { LessonDetail } from "@/types";

export const lessonService = {
  getLesson: (lessonId: string): Promise<LessonDetail> => apiClient.get<LessonDetail>(`/lessons/${lessonId}`),
};
