"use client";

import React from "react";

const CATEGORIES = ["ALL", "LEARNING", "STREAK", "XP", "MASTERY", "COURSE", "REVIEW"];

interface AchievementCategoryTabsProps {
  activeCategory: string;
  onSelectCategory: (category: string) => void;
}

export const AchievementCategoryTabs: React.FC<AchievementCategoryTabsProps> = ({
  activeCategory,
  onSelectCategory,
}) => {
  return (
    <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
      {CATEGORIES.map((cat) => {
        const isActive = activeCategory.toUpperCase() === cat;
        return (
          <button
            key={cat}
            onClick={() => onSelectCategory(cat)}
            className={`px-3 py-1.5 rounded-xl text-xs font-black uppercase tracking-wider transition-all whitespace-nowrap ${
              isActive
                ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
                : "bg-[#182830] text-gray-400 border border-[#37464f] hover:text-white hover:border-[#1cb0f6]/50"
            }`}
          >
            {cat === "COURSE" ? "COURSES" : cat}
          </button>
        );
      })}
    </div>
  );
};
