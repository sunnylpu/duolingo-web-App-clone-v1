"use client";

import React from "react";
import { HomeStreakSummary } from "@/services/home-service";
import { Card } from "@/components/ui/Card";

interface StreakCardProps {
  streak: HomeStreakSummary;
}

export const StreakCard: React.FC<StreakCardProps> = ({ streak }) => {
  const { current_streak = 0, longest_streak = 0, is_active_today = false } = streak;

  return (
    <Card className="p-5 bg-[#182830] border-2 border-[#37464f] space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🔥</span>
          <div>
            <h3 className="text-sm font-black uppercase text-white tracking-wider">
              {current_streak} Day Streak
            </h3>
            <p className="text-[11px] font-bold text-gray-400">
              Longest: {longest_streak} days
            </p>
          </div>
        </div>
        <span
          className={`px-2.5 py-1 text-[10px] uppercase font-black tracking-wider rounded-full border ${
            is_active_today
              ? "bg-[#ff9600]/20 text-[#ff9600] border-[#ff9600]/30"
              : "bg-gray-800 text-gray-400 border-gray-700"
          }`}
        >
          {is_active_today ? "Active Today" : "Complete Lesson"}
        </span>
      </div>
    </Card>
  );
};
