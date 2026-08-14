"use client";

import React from "react";
import { UserAchievement } from "@/services/achievement-service";
import { ProgressBar } from "@/components/ui/ProgressBar";

interface AchievementCardProps {
  item: UserAchievement;
}

const RARITY_THEMES: Record<string, { bg: string; text: string; border: string }> = {
  common: { bg: "bg-gray-500/20", text: "text-gray-300", border: "border-gray-500/30" },
  rare: { bg: "bg-[#1cb0f6]/20", text: "text-[#1cb0f6]", border: "border-[#1cb0f6]/30" },
  epic: { bg: "bg-[#a560ff]/20", text: "text-[#a560ff]", border: "border-[#a560ff]/30" },
  legendary: { bg: "bg-[#ffc800]/20", text: "text-[#ffc800]", border: "border-[#ffc800]/30" },
};

export const AchievementCard: React.FC<AchievementCardProps> = ({ item }) => {
  const { achievement, is_earned, progress, target } = item;
  const rarity = achievement.rarity || "common";
  const theme = RARITY_THEMES[rarity] || RARITY_THEMES.common;
  const pct = Math.min(100, Math.round((progress / Math.max(1, target)) * 100));

  return (
    <div
      className={`p-4 rounded-2xl border-2 transition-all flex items-start gap-4 ${
        is_earned
          ? "bg-[#182830] border-[#58cc02] shadow-md shadow-[#58cc02]/10"
          : "bg-[#131f24] border-[#37464f] opacity-80"
      }`}
    >
      <div
        className={`w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shrink-0 border ${
          is_earned
            ? "bg-[#58cc02]/20 border-[#58cc02]/40"
            : "bg-[#37464f]/40 border-[#37464f] grayscale"
        }`}
      >
        {is_earned ? achievement.icon : "🔒"}
      </div>

      <div className="flex-1 min-w-0 space-y-2">
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <h4 className="text-sm font-black text-white truncate">{achievement.name}</h4>
            <span
              className={`px-2 py-0.5 text-[9px] font-black uppercase tracking-wider rounded-full border ${theme.bg} ${theme.text} ${theme.border}`}
            >
              {rarity}
            </span>
          </div>
          {is_earned && (
            <span className="text-xs font-black text-[#58cc02] flex items-center gap-1">
              ✓ Earned
            </span>
          )}
        </div>

        <p className="text-xs text-gray-400 font-medium leading-relaxed">
          {achievement.description}
        </p>

        {!is_earned && (
          <div className="space-y-1 pt-1">
            <div className="flex items-center justify-between text-[10px] font-black text-gray-400">
              <span>Progress</span>
              <span>
                {progress} / {target} ({pct}%)
              </span>
            </div>
            <ProgressBar value={pct} height="h-2" />
          </div>
        )}

        {achievement.xp_reward > 0 && (
          <div className="text-[10px] font-black text-[#ffc800] pt-0.5">
            + {achievement.xp_reward} Bonus XP
          </div>
        )}
      </div>
    </div>
  );
};
