import React from "react";

interface CrownIndicatorProps {
  level: number;
  size?: "sm" | "md" | "lg";
}

export const CrownIndicator: React.FC<CrownIndicatorProps> = ({
  level,
  size = "md",
}) => {
  if (level <= 0) return null;

  const sizeClasses = {
    sm: "px-1.5 py-0.5 text-[10px]",
    md: "px-2 py-0.5 text-xs",
    lg: "px-2.5 py-1 text-sm",
  };

  return (
    <div
      className={`inline-flex items-center gap-1 bg-[#ffc800] text-black font-black rounded-full shadow-[0_2px_0_#cca000] ${sizeClasses[size]}`}
      title={`Crown Level ${level}`}
    >
      <span>👑</span>
      <span>{level}</span>
    </div>
  );
};
