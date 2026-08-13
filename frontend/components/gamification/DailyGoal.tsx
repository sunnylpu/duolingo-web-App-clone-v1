import React from "react";

interface DailyGoalProps {
  dailyXp: number;
  dailyGoalXp: number;
  isCompleted?: boolean;
}

export const DailyGoal: React.FC<DailyGoalProps> = ({
  dailyXp,
  dailyGoalXp,
  isCompleted = false,
}) => {
  const percent = Math.min(100, Math.round((dailyXp / Math.max(1, dailyGoalXp)) * 100));
  const completed = isCompleted || dailyXp >= dailyGoalXp;

  return (
    <div className="p-4 bg-[#182830] border-2 border-[#37464f] rounded-2xl space-y-3 select-none">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-lg">🎯</span>
          <span className="text-xs font-black uppercase text-white tracking-wider">Today's Goal</span>
        </div>
        {completed ? (
          <span className="text-[11px] font-black text-[#58cc02] bg-[#58cc02]/20 border border-[#58cc02] px-2 py-0.5 rounded-full flex items-center gap-1">
            <span>✓</span> Complete
          </span>
        ) : (
          <span className="text-xs font-black text-gray-400">
            {dailyXp} / {dailyGoalXp} XP
          </span>
        )}
      </div>

      <div className="h-3.5 bg-[#131f24] rounded-full overflow-hidden border border-[#37464f]">
        <div
          className={`h-full rounded-full transition-all duration-700 ease-out ${
            completed ? "bg-[#58cc02]" : "bg-[#ffc800]"
          }`}
          style={{ width: `${percent}%` }}
        />
      </div>

      <div className="flex justify-between text-[11px] font-bold text-gray-400">
        <span>{dailyXp} XP earned today</span>
        <span>Target: {dailyGoalXp} XP</span>
      </div>
    </div>
  );
};
