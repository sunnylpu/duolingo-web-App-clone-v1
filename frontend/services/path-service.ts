import { apiClient } from "@/lib/api-client";
import { PathResponse } from "@/types";

export interface SkillPerformance {
  skill_id: string;
  title: string;
  completion_percent: number;
  accuracy_percent: number;
  mastery_score: number;
  mastery_state: "weak" | "developing" | "strong" | "mastered";
  attempts: number;
  correct: number;
  incorrect: number;
  recommended_difficulty: number;
}

export const pathService = {
  getLearningPath: (courseId?: string): Promise<PathResponse> => {
    const query = courseId ? `?course_id=${encodeURIComponent(courseId)}` : "";
    return apiClient.get<PathResponse>(`/path${query}`);
  },
  getSkillPerformance: (skillId: string): Promise<SkillPerformance> => {
    return apiClient.get<SkillPerformance>(`/progress/skills/${skillId}`);
  },
};
