"use client";

import React from "react";
import { DailyQuestsResponse } from "@/services/quest-service";
import { DailyQuestCard } from "./DailyQuestCard";
import { Card } from "@/components/ui/Card";

interface DailyQuestListProps {
  data: DailyQuestsResponse | null;
  loading?: boolean;
}

export const DailyQuestList: React.FC<DailyQuestListProps> = ({ data, loading }) => {
  if (loading) {
    return (
      <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-3 animate-pulse">
        <div className="h-5 w-36 bg-[#131f24] rounded-lg" />
        <div className="space-y-3">
          <div className="h-20 bg-[#131f24] rounded-2xl" />
          <div className="h-20 bg-[#131f24] rounded-2xl" />
          <div className="h-20 bg-[#131f24] rounded-2xl" />
        </div>
      </Card>
    );
  }

  if (!data || data.quests.length === 0) {
    return (
      <Card className="p-6 bg-[#182830] border-2 border-[#37464f] text-center space-y-2">
        <div className="text-3xl">🎯</div>
        <h4 className="text-sm font-black text-white">Daily Quests Ready</h4>
        <p className="text-xs text-gray-400">
          Complete daily lessons to automatically unlock quest XP bonuses!
        </p>
      </Card>
    );
  }

  const completedCount = data.quests.filter((q) => q.completed).length;

  return (
    <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-black text-white uppercase tracking-wider flex items-center gap-2">
            <span>🎯</span>
            <span>Today&apos;s Quests</span>
          </h3>
          <p className="text-xs text-gray-400 font-medium mt-0.5">
            Complete daily missions to score extra XP
          </p>
        </div>

        <span className="text-xs font-black text-[#1cb0f6] bg-[#131f24] px-3 py-1 rounded-xl border border-[#37464f]">
          {completedCount} / {data.quests.length} Completed
        </span>
      </div>

      <div className="space-y-3">
        {data.quests.map((quest) => (
          <DailyQuestCard key={quest.id} quest={quest} />
        ))}
      </div>
    </Card>
  );
};
