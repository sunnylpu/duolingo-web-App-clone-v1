import React from "react";

interface ProgressBarProps {
  value: number; // 0 to 100
  color?: string;
  height?: string;
  showPercentage?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  color = "bg-[#58cc02]",
  height = "h-3",
  showPercentage = false,
}) => {
  const percentage = Math.min(100, Math.max(0, value));

  return (
    <div className="w-full space-y-1">
      {showPercentage && (
        <div className="flex justify-between text-xs text-gray-400 font-bold">
          <span>Progress</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      <div className={`w-full bg-[#37464f] rounded-full overflow-hidden ${height}`}>
        <div
          className={`${color} ${height} rounded-full transition-all duration-300`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
