import { fetchApi, checkBackendHealth } from "@/lib/api-client";

export const apiService = {
  checkHealth: checkBackendHealth,
  getUsers: () => fetchApi("/users"),
  getCourses: () => fetchApi("/courses"),
  getLessons: () => fetchApi("/lessons"),
  getLeaderboard: (league = "Bronze") => fetchApi(`/leaderboard?league=${league}`),
  getGamification: (userId: string) => fetchApi(`/gamification/users/${userId}`),
};
