import { apiClient } from "@/lib/api-client";
import { Achievement, UserAchievement } from "@/types";

export const achievementService = {
  getAchievements: (): Promise<Achievement[]> => apiClient.get<Achievement[]>("/achievements"),
  getMyAchievements: (): Promise<UserAchievement[]> => apiClient.get<UserAchievement[]>("/users/me/achievements"),
};
