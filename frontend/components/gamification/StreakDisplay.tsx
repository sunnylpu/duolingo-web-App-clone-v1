import React from "react";

interface StreakDisplayProps {
  currentStreak: number;
  longestStreak?: number;
  className?: string;
  showLongest?: boolean;
}

export const StreakDisplay: React.FC<StreakDisplayProps> = ({
  currentStreak,
  longestStreak,
  className = "",
  showLongest = false,
}) => {
  return (
    <div
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#ff9600]/10 border border-[#ff9600]/30 rounded-xl text-[#ff9600] font-black text-sm select-none ${className}`}
      title={longestStreak ? `Current Streak: ${currentStreak}d (Best: ${longestStreak}d)` : `Current Streak: ${currentStreak} days`}
    >
      <span className="text-base animate-pulse">🔥</span>
      <span>{currentStreak}</span>
      {showLongest && longestStreak !== undefined && (
        <span className="text-xs text-gray-400 font-normal">
          (Best: {longestStreak})
        </span>
      )}
    </div>
  );
};
