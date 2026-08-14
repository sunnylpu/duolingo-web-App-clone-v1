"use client";

import React from "react";
import { FriendSuggestion } from "@/services/social-service";
import { FriendCard } from "./FriendCard";

interface FriendSuggestionsProps {
  suggestions: FriendSuggestion[];
  onRefresh?: () => void;
}

export const FriendSuggestions: React.FC<FriendSuggestionsProps> = ({
  suggestions,
  onRefresh,
}) => {
  if (suggestions.length === 0) return null;

  return (
    <div className="space-y-3">
      <h3 className="text-xs font-black uppercase text-gray-400 tracking-wider flex items-center justify-between">
        <span>Suggested Learners</span>
        <span className="text-[10px] text-[#1cb0f6] font-bold">Based on Leaderboard</span>
      </h3>

      <div className="space-y-3">
        {suggestions.map((item) => (
          <FriendCard
            key={item.user.id}
            user={item.user}
            onFollowToggle={onRefresh}
          />
        ))}
      </div>
    </div>
  );
};
