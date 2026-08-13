import { SkillStatus } from "./path";

export interface SkillProgressSummary {
  skill_id: string;
  status: SkillStatus;
  completion_percent: number;
  crown_level: number;
  lessons_completed: number;
  xp_earned: number;
}

export interface ProgressResponse {
  skills: SkillProgressSummary[];
}
