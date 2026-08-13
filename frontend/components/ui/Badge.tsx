import React from "react";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "green" | "blue" | "purple" | "yellow" | "gray";
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "green",
  className = "",
}) => {
  const variantMap = {
    green: "bg-[#58cc02]/10 text-[#58cc02] border-[#58cc02]/30",
    blue: "bg-[#1cb0f6]/10 text-[#1cb0f6] border-[#1cb0f6]/30",
    purple: "bg-[#ce82ff]/10 text-[#ce82ff] border-[#ce82ff]/30",
    yellow: "bg-[#ffc800]/10 text-[#ffc800] border-[#ffc800]/30",
    gray: "bg-gray-800 text-gray-400 border-gray-700",
  };

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-extrabold border uppercase tracking-wider ${variantMap[variant]} ${className}`}
    >
      {children}
    </span>
  );
};
