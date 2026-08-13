import { apiClient } from "@/lib/api-client";
import { User, UserStats, UserProfile } from "@/types";

export const userService = {
  getCurrentUser: (): Promise<User> => apiClient.get<User>("/users/me"),
  getUserStats: (): Promise<UserStats> => apiClient.get<UserStats>("/users/me/stats"),
  getUserProfile: (): Promise<UserProfile> => apiClient.get<UserProfile>("/users/me/profile"),
};
