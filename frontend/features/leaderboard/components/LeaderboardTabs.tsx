import React from "react";
import { LeaderboardPeriod } from "@/types";

interface LeaderboardTabsProps {
  activePeriod: LeaderboardPeriod;
  onChange: (period: LeaderboardPeriod) => void;
}

export const LeaderboardTabs: React.FC<LeaderboardTabsProps> = ({
  activePeriod,
  onChange,
}) => {
  const tabs: { id: LeaderboardPeriod; label: string; icon: string }[] = [
    { id: "weekly", label: "Weekly League", icon: "⚡" },
    { id: "monthly", label: "Monthly Standings", icon: "📅" },
    { id: "all_time", label: "All-Time Hall of Fame", icon: "👑" },
  ];

  return (
    <div className="flex bg-[#131f24] p-1.5 rounded-2xl border border-[#37464f] select-none">
      {tabs.map((tab) => {
        const isActive = activePeriod === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            role="tab"
            aria-selected={isActive}
            className={`flex-1 flex items-center justify-center gap-2 py-3 px-3 rounded-xl text-xs sm:text-sm font-extrabold transition-all cursor-pointer ${
              isActive
                ? "bg-[#1cb0f6] text-white shadow-[0_3px_0_#1899d6]"
                : "text-gray-400 hover:text-gray-200 hover:bg-[#182830]"
            }`}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
};
