import React from "react";

interface HeartDisplayProps {
  hearts: number;
  maxHearts?: number;
  size?: "sm" | "md" | "lg";
  onClick?: () => void;
}

export const HeartDisplay: React.FC<HeartDisplayProps> = ({
  hearts,
  maxHearts = 5,
  size = "md",
  onClick,
}) => {
  const heartIcons = Array.from({ length: maxHearts }, (_, i) => i < hearts);

  const sizeClasses = {
    sm: "text-base gap-1",
    md: "text-xl gap-1.5",
    lg: "text-3xl gap-2",
  };

  return (
    <button
      onClick={onClick}
      disabled={!onClick}
      aria-label={`${hearts} of ${maxHearts} hearts remaining. Click for heart info.`}
      className={`inline-flex items-center select-none ${sizeClasses[size]} ${
        onClick
          ? "cursor-pointer hover:scale-105 transition-transform focus:outline-none focus-visible:ring-2 focus-visible:ring-[#ff4b4b]"
          : "cursor-default"
      }`}
    >
      {heartIcons.map((filled, idx) => (
        <span
          key={idx}
          className={`transition-all duration-300 ${
            filled
              ? "text-[#ff4b4b] drop-shadow-[0_2px_0_#d32f2f] animate-pulse"
              : "text-gray-600 grayscale opacity-40"
          }`}
        >
          {filled ? "❤️" : "🖤"}
        </span>
      ))}
      <span className="font-black text-xs sm:text-sm text-[#ff4b4b] ml-1">
        {hearts}/{maxHearts}
      </span>
    </button>
  );
};
