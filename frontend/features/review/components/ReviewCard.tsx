"use client";

import React from "react";
import { Card } from "@/components/ui/Card";

interface ReviewCardProps {
  count: number;
  skillsCount: number;
  onStartReview: () => void;
}

export const ReviewCard: React.FC<ReviewCardProps> = ({
  count,
  skillsCount,
  onStartReview,
}) => {
  return (
    <Card className="p-5 bg-[#182830] border-2 border-[#1cb0f6] space-y-3 shadow-lg shadow-[#1cb0f6]/10">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="text-2xl">🔁</span>
          <div>
            <h3 className="text-sm font-black uppercase text-white tracking-wider">
              Smart Review
            </h3>
            <p className="text-xs text-gray-300 font-medium">
              {skillsCount > 0
                ? `You have ${skillsCount} skill${skillsCount > 1 ? "s" : ""} to review (${count} exercises)`
                : "Practice recent exercises to build retention"}
            </p>
          </div>
        </div>
        <button
          onClick={onStartReview}
          className="px-4 py-2 rounded-xl bg-[#1cb0f6] hover:bg-[#20bdff] text-black font-black text-xs tracking-wider shadow-[0_3px_0_#1899d6] active:translate-y-0.5 transition-all"
        >
          START REVIEW →
        </button>
      </div>
    </Card>
  );
};
