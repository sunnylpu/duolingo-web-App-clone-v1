import { CourseSummary } from "./course";

export type SkillStatus = "locked" | "available" | "in_progress" | "completed";

export interface SkillPath {
  id: string;
  title: string;
  description: string | null;
  order_index: number;
  xp_reward: number;
  prerequisite_skill_id: string | null;
  status: SkillStatus;
  completion_percent: number;
  crown_level: number;
}

export interface UnitPath {
  id: string;
  title: string;
  description: string | null;
  order_index: number;
  skills: SkillPath[];
}

export interface PathResponse {
  course: CourseSummary;
  units: UnitPath[];
}
