"use client";

import React from "react";

interface CourseProgressBadgeProps {
  progressPercent: number;
  completedSkills?: number;
  totalSkills?: number;
}

export const CourseProgressBadge: React.FC<CourseProgressBadgeProps> = ({
  progressPercent,
  completedSkills,
  totalSkills,
}) => {
  return (
    <div className="flex flex-col gap-1 text-xs">
      <div className="flex items-center justify-between text-slate-400 font-bold">
        {completedSkills !== undefined && totalSkills !== undefined ? (
          <span>
            {completedSkills} / {totalSkills} skills
          </span>
        ) : (
          <span>Progress</span>
        )}
        <span className="text-emerald-400 font-extrabold">{progressPercent}%</span>
      </div>
      <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden">
        <div
          className="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-300"
          style={{ width: `${Math.min(100, Math.max(0, progressPercent))}%` }}
        />
      </div>
    </div>
  );
};
