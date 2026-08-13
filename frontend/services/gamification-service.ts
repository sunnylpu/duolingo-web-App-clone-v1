import { apiClient } from "@/lib/api-client";
import { GamificationStats } from "@/types";

export const gamificationService = {
  getStats: (): Promise<GamificationStats> => apiClient.get<GamificationStats>("/gamification/stats"),
};
