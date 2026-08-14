import { apiClient } from "@/lib/api-client";

export interface Achievement {
  id: string;
  code: string;
  name: string;
  description: string;
  icon: string;
  category: string;
  rarity: "common" | "rare" | "epic" | "legendary";
  xp_reward: number;
  requirement_type: string;
  requirement_value: number;
  course_id?: string | null;
}

export interface UserAchievement {
  achievement: Achievement;
  is_earned: boolean;
  earned_at?: string | null;
  progress: number;
  target: number;
}

export const achievementService = {
  getMyAchievements: (category?: string): Promise<UserAchievement[]> => {
    const query =
      category && category.toLowerCase() !== "all"
        ? `?category=${encodeURIComponent(category.toLowerCase())}`
        : "";
    return apiClient.get<UserAchievement[]>(`/users/me/achievements${query}`);
  },
};
