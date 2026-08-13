import React from "react";
import { LeaderboardEntry } from "@/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

interface LeaderboardRowProps {
  entry: LeaderboardEntry;
}

export const LeaderboardRow: React.FC<LeaderboardRowProps> = ({ entry }) => {
  const { rank, display_name, username, xp, is_current_user } = entry;

  const getRankBadge = () => {
    if (rank === 1) return <span className="text-xl">🥇</span>;
    if (rank === 2) return <span className="text-xl">🥈</span>;
    if (rank === 3) return <span className="text-xl">🥉</span>;
    return <span className="text-sm font-black text-gray-400">#{rank}</span>;
  };

  return (
    <Card
      className={`p-3.5 flex items-center justify-between gap-4 transition-all select-none border-2 ${
        is_current_user
          ? "bg-[#182830] border-[#58cc02] shadow-[0_3px_0_#46a302]"
          : "bg-[#131f24] border-[#37464f] hover:border-gray-500"
      }`}
    >
      <div className="flex items-center gap-3.5 min-w-0">
        {/* Rank Position */}
        <div className="w-8 flex items-center justify-center shrink-0">
          {getRankBadge()}
        </div>

        {/* User Avatar */}
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center font-black text-sm shrink-0 border-2 ${
            is_current_user
              ? "bg-[#58cc02] text-black border-[#46a302]"
              : "bg-[#37464f] text-white border-[#2b373e]"
          }`}
        >
          {display_name.charAt(0)}
        </div>

        {/* User Metadata */}
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-sm text-white truncate">
              {display_name}
            </span>
            {is_current_user && <Badge variant="green">YOU</Badge>}
          </div>
          <span className="text-xs text-gray-400 font-medium block truncate">
            @{username}
          </span>
        </div>
      </div>

      {/* XP Score */}
      <div className="text-right shrink-0">
        <span className="text-sm font-black text-[#ffc800]">⭐ {xp} XP</span>
      </div>
    </Card>
  );
};
