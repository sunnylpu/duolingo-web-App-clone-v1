import React from "react";
import { Card } from "@/components/ui/Card";

interface DailyActivitySummaryProps {
  xpEarned: number;
  lessonsCompleted: number;
  goalXp: number;
  goalCompleted: boolean;
  dateStr?: string;
}

export const DailyActivitySummary: React.FC<DailyActivitySummaryProps> = ({
  xpEarned,
  lessonsCompleted,
  goalXp,
  goalCompleted,
  dateStr = "Today",
}) => {
  return (
    <Card className="p-4 bg-[#182830] border-2 border-[#37464f] space-y-3 select-none">
      <div className="flex items-center justify-between text-xs font-black text-white">
        <span className="uppercase tracking-wider">Daily Activity</span>
        <span className="text-gray-400 font-normal">{dateStr}</span>
      </div>

      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="p-2 bg-[#131f24] rounded-xl border border-[#37464f]">
          <div className="text-[10px] text-gray-400 font-bold uppercase">XP</div>
          <div className="text-sm font-black text-[#ffc800] mt-0.5">⭐ {xpEarned}</div>
        </div>

        <div className="p-2 bg-[#131f24] rounded-xl border border-[#37464f]">
          <div className="text-[10px] text-gray-400 font-bold uppercase">Lessons</div>
          <div className="text-sm font-black text-[#1cb0f6] mt-0.5">📚 {lessonsCompleted}</div>
        </div>

        <div className="p-2 bg-[#131f24] rounded-xl border border-[#37464f]">
          <div className="text-[10px] text-gray-400 font-bold uppercase">Goal</div>
          <div className={`text-sm font-black mt-0.5 ${goalCompleted ? "text-[#58cc02]" : "text-gray-300"}`}>
            {goalCompleted ? "✓ Done" : `${xpEarned}/${goalXp}`}
          </div>
        </div>
      </div>
    </Card>
  );
};
