import { apiClient } from "@/lib/api-client";
import { Exercise } from "@/types";

export interface ReviewSkillSummary {
  skill_id: string;
  title: string;
  accuracy_percent: number;
  reason: string;
}

export interface ReviewExerciseDetail extends Exercise {
  skill_id: string;
  previous_user_answer?: string | null;
}

export interface ReviewResponse {
  available: boolean;
  count: number;
  skills: ReviewSkillSummary[];
  exercises: ReviewExerciseDetail[];
}

export const reviewService = {
  getSmartReview: (courseId?: string): Promise<ReviewResponse> => {
    const params = courseId ? `?course_id=${encodeURIComponent(courseId)}` : "";
    return apiClient.get<ReviewResponse>(`/review${params}`);
  },
};
