"use client";

import React from "react";
import { QuestItem } from "@/services/quest-service";

interface DailyQuestCardProps {
  quest: QuestItem;
}

const TYPE_ICONS: Record<string, string> = {
  LESSONS_COMPLETED: "📚",
  XP_EARNED: "⭐",
  CORRECT_ANSWERS: "🎯",
  SKILLS_COMPLETED: "🔮",
  REVIEWS_COMPLETED: "🔄",
};

export const DailyQuestCard: React.FC<DailyQuestCardProps> = ({ quest }) => {
  const icon = TYPE_ICONS[quest.quest_type] || "🎯";
  const progressPct = Math.min(
    100,
    Math.round((quest.current_value / quest.target_value) * 100)
  );

  return (
    <div
      className={`p-4 bg-[#182830] border-2 rounded-2xl flex flex-col justify-between space-y-3 transition-all ${
        quest.completed
          ? "border-[#58cc02] bg-[#182830]/90"
          : "border-[#37464f] hover:border-[#1cb0f6]"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#131f24] border border-[#37464f] flex items-center justify-center text-xl shrink-0">
            {icon}
          </div>
          <div>
            <h4 className="text-xs font-black text-white flex items-center gap-2">
              <span>{quest.title}</span>
            </h4>
            <p className="text-[11px] text-gray-400 font-medium mt-0.5">
              {quest.description}
            </p>
          </div>
        </div>

        <div className="shrink-0 text-right">
          {quest.completed ? (
            <span className="text-xs font-black text-[#58cc02] flex items-center gap-1 bg-[#58cc02]/10 px-2 py-1 rounded-lg border border-[#58cc02]/30">
              ✓ Done
            </span>
          ) : (
            <span className="text-xs font-black text-[#ffc800] bg-[#ffc800]/10 px-2 py-1 rounded-lg border border-[#ffc800]/30">
              +{quest.reward_xp} XP
            </span>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1">
        <div className="flex justify-between items-center text-[10px] font-bold text-gray-400">
          <span>PROGRESS</span>
          <span>
            {quest.current_value} / {quest.target_value}
          </span>
        </div>

        <div className="w-full bg-[#131f24] h-2.5 rounded-full overflow-hidden border border-[#37464f] p-0.5">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              quest.completed ? "bg-[#58cc02]" : "bg-[#1cb0f6]"
            }`}
            style={{ width: `${progressPct}%` }}
          />
        </div>
      </div>
    </div>
  );
};
