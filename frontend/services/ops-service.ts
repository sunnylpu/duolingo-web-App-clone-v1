import { apiClient } from "@/lib/api-client";

export interface OpsOverviewResponse {
  users: {
    total: number;
    active_today: number;
  };
  courses: {
    total: number;
  };
  learning: {
    lessons_completed_today: number;
    exercises_answered_today: number;
    correct_answer_pct: number;
  };
  gamification: {
    xp_awarded_today: number;
    achievements_unlocked_today: number;
  };
  system: {
    requests_total: number;
    errors_total: number;
    database_status: string;
    version: string;
    environment: string;
  };
}

export const opsService = {
  getOverview: (): Promise<OpsOverviewResponse> => {
    return apiClient.get<OpsOverviewResponse>("/ops/overview");
  },
};
