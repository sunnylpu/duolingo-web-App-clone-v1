"use client";

import React from "react";
import { HomeDailyGoalSummary } from "@/services/home-service";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";

interface DailyGoalCardProps {
  dailyGoal: HomeDailyGoalSummary;
}

export const DailyGoalCard: React.FC<DailyGoalCardProps> = ({ dailyGoal }) => {
  const { xp = 0, goal = 30, goal_completed = false } = dailyGoal;
  const pct = Math.min(100, Math.round((xp / goal) * 100));
  const remaining = Math.max(0, goal - xp);

  return (
    <Card className="p-5 bg-[#182830] border-2 border-[#37464f] space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-xl">🎯</span>
          <h3 className="text-sm font-black uppercase text-white tracking-wider">
            Today's Goal
          </h3>
        </div>
        {goal_completed ? (
          <span className="px-2.5 py-0.5 text-[10px] uppercase font-black tracking-wider rounded-full bg-[#58cc02]/20 text-[#58cc02] border border-[#58cc02]/30">
            ✓ Goal Met
          </span>
        ) : (
          <span className="text-xs font-black text-[#ffc800]">
            {remaining} XP to go
          </span>
        )}
      </div>

      <div className="space-y-1">
        <div className="flex justify-between text-xs font-bold text-gray-400">
          <span>Daily Progress</span>
          <span className="text-white">{xp} / {goal} XP</span>
        </div>
        <ProgressBar value={pct} height="h-3" color={goal_completed ? "bg-[#58cc02]" : "bg-[#ffc800]"} />
      </div>
    </Card>
  );
};
