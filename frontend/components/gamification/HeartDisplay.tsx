import React from "react";

interface HeartDisplayProps {
  hearts: number;
  maxHearts?: number;
  showText?: boolean;
  className?: string;
}

export const HeartDisplay: React.FC<HeartDisplayProps> = ({
  hearts,
  maxHearts = 5,
  showText = true,
  className = "",
}) => {
  const safeHearts = Math.max(0, hearts);

  return (
    <div
      className={`flex items-center gap-1.5 font-black text-[#ff4b4b] select-none ${className}`}
      aria-label={`${safeHearts} of ${maxHearts} hearts remaining`}
    >
      <span className="text-xl transition-transform duration-300 motion-safe:animate-pulse">
        ❤️
      </span>
      {showText && <span className="text-sm sm:text-base font-extrabold">{safeHearts}</span>}
    </div>
  );
};
