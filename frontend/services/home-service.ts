import { apiClient } from "@/lib/api-client";
import { CourseSummary } from "@/types";

export interface ContinueLearningSummary {
  unit_id?: string | null;
  unit_title?: string | null;
  skill_id?: string | null;
  skill_title?: string | null;
  lesson_id?: string | null;
  lesson_title?: string | null;
  progress_percent: number;
  lessons_completed: number;
  total_lessons: number;
}

export interface HomeDailyGoalSummary {
  xp: number;
  goal: number;
  goal_completed: boolean;
  goal_just_completed: boolean;
}

export interface HomeStreakSummary {
  current_streak: number;
  longest_streak: number;
  is_active_today: boolean;
}

export interface HomeHeartsSummary {
  hearts: number;
  max_hearts: number;
  next_heart_refill_seconds?: number | null;
}

export interface HomeDashboardResponse {
  course: CourseSummary;
  continue_learning: ContinueLearningSummary;
  daily_goal: HomeDailyGoalSummary;
  streak: HomeStreakSummary;
  hearts: HomeHeartsSummary;
  courses: CourseSummary[];
}

export const homeService = {
  getHomeDashboard: (courseId?: string): Promise<HomeDashboardResponse> => {
    const params = courseId ? `?course_id=${encodeURIComponent(courseId)}` : "";
    return apiClient.get<HomeDashboardResponse>(`/home${params}`);
  },
};
