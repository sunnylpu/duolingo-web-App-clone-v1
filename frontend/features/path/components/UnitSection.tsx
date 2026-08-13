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
  // Compute overall unit completion percentage
  const totalSkills = unit.skills.length;
  const completedSkills = unit.skills.filter(
    (s) => s.status === "completed"
  ).length;
  const unitPercentage =
    totalSkills > 0 ? Math.round((completedSkills / totalSkills) * 100) : 0;

  return (
    <div className="space-y-6 mb-12">
      {/* Unit Header Card */}
      <div className="duo-card p-5 bg-[#182830] border-2 border-[#37464f] relative overflow-hidden">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="green">Unit {unit.order_index}</Badge>
              <span className="text-xs font-bold text-gray-400">
                {completedSkills} / {totalSkills} Skills Mastered
              </span>
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
              <span>{unitPercentage}%</span>
            </div>
            <ProgressBar value={unitPercentage} height="h-3" color="bg-[#58cc02]" />
          </div>
        </div>
      </div>

      {/* Vertical Learning Path Skills Chain */}
      <div className="flex flex-col items-center max-w-md mx-auto py-2">
        {unit.skills.map((skill, index) => {
          // Calculate subtle sine-wave offset pattern for path nodes
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
      </div>
    </div>
  );
};
