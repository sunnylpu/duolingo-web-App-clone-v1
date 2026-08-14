import React from "react";
import { UnitPath, SkillPath } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { SkillNode } from "./SkillNode";
import { PathConnector } from "./PathConnector";

interface UnitSectionProps {
  unit: UnitPath;
  onSelectSkill: (skill: SkillPath) => void;
}

export const UnitSection: React.FC<UnitSectionProps> = ({
  unit,
  onSelectSkill,
}) => {
  const totalSkills = unit.total_skills ?? unit.skills.length;
  const completedSkills = unit.completed_skills ?? unit.skills.filter(
    (s) => s.status === "completed"
  ).length;
  const unitPercentage =
    unit.completion_percent !== undefined
      ? Math.round(unit.completion_percent)
      : totalSkills > 0
      ? Math.round((completedSkills / totalSkills) * 100)
      : 0;

  const isCompleted = unit.status === "completed" || unitPercentage >= 100;

  return (
    <div className="space-y-6 mb-12">
      {/* Unit Header Card */}
      <div className="duo-card p-5 bg-[#182830] border-2 border-[#37464f] relative overflow-hidden">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Badge variant={isCompleted ? "green" : "blue"}>Unit {unit.order_index}</Badge>
              <span className="text-xs font-bold text-gray-400">
                {completedSkills} / {totalSkills} Skills Mastered
              </span>
              {isCompleted && (
                <span className="px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded-full bg-[#58cc02]/20 text-[#58cc02] border border-[#58cc02]/30">
                  ✓ Unit Complete
                </span>
              )}
            </div>
            <h2 className="text-xl sm:text-2xl font-black text-white">
              {unit.title}
            </h2>
            {unit.description && (
              <p className="text-xs sm:text-sm text-gray-400 mt-1 max-w-lg">
                {unit.description}
              </p>
            )}
          </div>

          <div className="sm:w-36 space-y-1">
            <div className="flex justify-between text-xs text-gray-400 font-bold">
              <span>Unit Progress</span>
              <span className={isCompleted ? "text-[#58cc02]" : "text-white"}>{unitPercentage}%</span>
            </div>
            <ProgressBar value={unitPercentage} height="h-3" color="bg-[#58cc02]" />
          </div>
        </div>
      </div>

      {/* Vertical Learning Path Skills Chain */}
      <div className="flex flex-col items-center max-w-md mx-auto py-2">
        {unit.skills.map((skill, index) => {
          const offsets: ("center" | "left" | "right")[] = [
            "center",
            "left",
            "center",
            "right",
          ];
          const offset = offsets[index % offsets.length];

          return (
            <React.Fragment key={skill.id}>
              {index > 0 && <PathConnector offset={offset} />}
              <div
                className={`transition-all ${
                  offset === "left"
                    ? "-translate-x-6 sm:-translate-x-10"
                    : offset === "right"
                    ? "translate-x-6 sm:translate-x-10"
                    : ""
                }`}
              >
                <SkillNode skill={skill} onSelect={onSelectSkill} />
              </div>
            </React.Fragment>
          );
        })}

        {/* Unit Completion Milestone Node */}
        <PathConnector offset="center" />
        <div
          className={`w-full max-w-sm px-5 py-3 rounded-2xl border-2 flex items-center justify-between shadow-lg transition-all ${
            isCompleted
              ? "bg-[#58cc02]/20 border-[#58cc02] text-[#58cc02] shadow-[#58cc02]/10"
              : "bg-[#182830] border-[#37464f] text-gray-400"
          }`}
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl" role="img" aria-label="Trophy">
              🏆
            </span>
            <div className="text-left">
              <div className="text-xs uppercase font-black tracking-wider">
                {isCompleted ? "Unit Complete (+50 XP)" : `Unit ${unit.order_index} Milestone`}
              </div>
              <div className="text-sm font-extrabold text-white">
                {isCompleted ? "Foundations Mastered" : `${completedSkills} / ${totalSkills} Skills Completed`}
              </div>
            </div>
          </div>
          {isCompleted && (
            <span className="text-xs font-black uppercase text-[#58cc02] bg-[#58cc02]/20 px-2.5 py-1 rounded-full border border-[#58cc02]/30">
              Claimed
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
