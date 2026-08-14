"use client";

import React from "react";
import { WeeklyChallengeResponse } from "@/services/quest-service";
import { Card } from "@/components/ui/Card";

interface WeeklyChallengeCardProps {
  data: WeeklyChallengeResponse | null;
  loading?: boolean;
}

export const WeeklyChallengeCard: React.FC<WeeklyChallengeCardProps> = ({ data, loading }) => {
  if (loading || !data || !data.challenge) return null;

  const challenge = data.challenge;
  const progressPct = Math.min(
    100,
    Math.round((challenge.current_value / challenge.target_value) * 100)
  );

  return (
    <Card className="p-6 bg-gradient-to-br from-[#182830] to-[#131f24] border-2 border-[#ffc800]/50 space-y-4 shadow-xl">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-[#ffc800]/10 border border-[#ffc800]/40 flex items-center justify-center text-2xl shrink-0">
            🏆
          </div>
          <div>
            <span className="text-[10px] font-black uppercase tracking-wider text-[#ffc800]">
              Weekly Challenge
            </span>
            <h3 className="text-sm font-black text-white mt-0.5">
              {challenge.title}
            </h3>
            <p className="text-xs text-gray-400 font-medium mt-0.5">
              {challenge.description}
            </p>
          </div>
        </div>

        <div className="shrink-0 text-right">
          {challenge.completed ? (
            <span className="text-xs font-black text-[#58cc02] bg-[#58cc02]/10 px-3 py-1.5 rounded-xl border border-[#58cc02]/30">
              ✓ Mastered!
            </span>
          ) : (
            <span className="text-xs font-black text-[#ffc800] bg-[#ffc800]/10 px-3 py-1.5 rounded-xl border border-[#ffc800]/30">
              +{challenge.reward_xp} XP
            </span>
          )}
        </div>
      </div>

      <div className="space-y-1">
        <div className="flex justify-between items-center text-xs font-bold text-gray-400">
          <span>WEEKLY PROGRESS</span>
          <span className="text-white">
            {challenge.current_value} / {challenge.target_value}
          </span>
        </div>

        <div className="w-full bg-[#131f24] h-3 rounded-full overflow-hidden border border-[#37464f] p-0.5">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              challenge.completed ? "bg-[#58cc02]" : "bg-[#ffc800]"
            }`}
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </div>
    </Card>
  );
};
