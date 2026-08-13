import { checkBackendHealth } from "@/lib/api-client";
import { userService } from "./user-service";
import { courseService } from "./course-service";
import { pathService } from "./path-service";
import { lessonService } from "./lesson-service";
import { progressService } from "./progress-service";
import { gamificationService } from "./gamification-service";
import { leaderboardService } from "./leaderboard-service";
import { achievementService } from "./achievement-service";

export const apiService = {
  checkHealth: checkBackendHealth,
  user: userService,
  course: courseService,
  path: pathService,
  lesson: lessonService,
  progress: progressService,
  gamification: gamificationService,
  leaderboard: leaderboardService,
  achievement: achievementService,
};

export * from "./user-service";
export * from "./course-service";
export * from "./path-service";
export * from "./lesson-service";
export * from "./progress-service";
export * from "./gamification-service";
export * from "./leaderboard-service";
export * from "./achievement-service";
