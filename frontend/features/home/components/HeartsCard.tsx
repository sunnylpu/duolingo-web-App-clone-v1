"use client";

import React from "react";
import { HomeHeartsSummary } from "@/services/home-service";
import { Card } from "@/components/ui/Card";

interface HeartsCardProps {
  hearts: HomeHeartsSummary;
  onPracticeClick?: () => void;
}

export const HeartsCard: React.FC<HeartsCardProps> = ({
  hearts,
  onPracticeClick,
}) => {
  const currentHearts = hearts.hearts ?? 5;
  const maxHearts = hearts.max_hearts ?? 5;

  return (
    <Card className="p-5 bg-[#182830] border-2 border-[#37464f] space-y-2">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl">❤️</span>
          <div>
            <h3 className="text-sm font-black uppercase text-white tracking-wider">
              {currentHearts} / {maxHearts} Hearts
            </h3>
            <p className="text-[11px] font-bold text-gray-400">
              {currentHearts < maxHearts ? "Refills over time or by practice" : "Full energy!"}
            </p>
          </div>
        </div>

        {onPracticeClick && (
          <button
            onClick={onPracticeClick}
            className="px-3 py-1.5 rounded-xl bg-[#ff4b4b]/20 hover:bg-[#ff4b4b]/30 border border-[#ff4b4b]/30 text-xs font-black text-[#ff4b4b] transition-all"
          >
            {currentHearts < maxHearts ? "PRACTICE +1 ❤️" : "PRACTICE"}
          </button>
        )}
      </div>
    </Card>
  );
};
