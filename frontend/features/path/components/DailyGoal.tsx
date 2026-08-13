import React from "react";
import { UserStats } from "@/types";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Badge } from "@/components/ui/Badge";

interface DailyGoalProps {
  stats: UserStats;
}

export const DailyGoal: React.FC<DailyGoalProps> = ({ stats }) => {
  const percentage = Math.min(
    100,
    Math.round((stats.daily_xp / stats.daily_goal_xp) * 100)
  );

  return (
    <div className="duo-card p-4 mb-6 space-y-2">
      <div className="flex justify-between items-center text-sm font-extrabold">
        <div className="flex items-center gap-2">
          <span>⚡</span>
          <span className="text-gray-200">Today&apos;s Goal</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400 font-mono">
            {stats.daily_xp} / {stats.daily_goal_xp} XP
          </span>
          <Badge variant={percentage >= 100 ? "green" : "yellow"}>
            {percentage >= 100 ? "Goal Reached!" : `${percentage}%`}
          </Badge>
        </div>
      </div>
      <ProgressBar value={percentage} height="h-3" />
    </div>
  );
};
