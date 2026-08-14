"use client";

import React from "react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: string;
  color?: "green" | "blue" | "yellow" | "red" | "purple";
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon,
  color = "blue",
}) => {
  const COLOR_CLASSES = {
    green: "border-[#58cc02]/30 text-[#58cc02]",
    blue: "border-[#1cb0f6]/30 text-[#1cb0f6]",
    yellow: "border-[#ffc800]/30 text-[#ffc800]",
    red: "border-[#ff4b4b]/30 text-[#ff4b4b]",
    purple: "border-[#ce82ff]/30 text-[#ce82ff]",
  };

  return (
    <div className="p-5 bg-[#182830] border-2 border-[#37464f] rounded-2xl flex items-center justify-between gap-4">
      <div>
        <span className="text-[11px] font-black uppercase text-gray-400 tracking-wider">
          {title}
        </span>
        <h4 className={`text-2xl font-black mt-1 ${COLOR_CLASSES[color].split(" ")[1]}`}>
          {value}
        </h4>
        {subtitle && (
          <p className="text-[11px] text-gray-400 font-medium mt-0.5">{subtitle}</p>
        )}
      </div>

      <div
        className={`w-12 h-12 rounded-2xl bg-[#131f24] border flex items-center justify-center text-2xl shrink-0 ${
          COLOR_CLASSES[color].split(" ")[0]
        }`}
      >
        {icon}
      </div>
    </div>
  );
};
