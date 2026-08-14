"use client";

import React from "react";
import Link from "next/link";
import { UserSocialSummary } from "@/services/social-service";
import { FollowButton } from "./FollowButton";

interface FriendCardProps {
  user: UserSocialSummary;
  onFollowToggle?: () => void;
}

export const FriendCard: React.FC<FriendCardProps> = ({ user, onFollowToggle }) => {
  return (
    <div className="p-4 bg-[#182830] border-2 border-[#37464f] rounded-2xl flex items-center justify-between gap-4">
      <Link href={`/profile/${user.id}`} className="flex items-center gap-3.5 min-w-0 group">
        <div className="w-12 h-12 rounded-full bg-[#58cc02] flex items-center justify-center text-black font-black text-xl shrink-0 group-hover:scale-105 transition-transform">
          {user.avatar || user.display_name.charAt(0)}
        </div>
        <div className="min-w-0">
          <h4 className="text-sm font-black text-white group-hover:text-[#1cb0f6] transition-colors truncate">
            {user.display_name}
          </h4>
          <p className="text-xs text-gray-400 font-medium truncate">@{user.username}</p>
          <div className="flex items-center gap-2 text-[10px] font-black text-[#ffc800] mt-0.5">
            <span>⭐ {user.total_xp} XP</span>
            <span>•</span>
            <span className="text-[#ff9600]">🔥 {user.current_streak}d</span>
          </div>
        </div>
      </Link>

      <FollowButton
        userId={user.id}
        initialIsFollowing={user.is_following}
        onToggle={onFollowToggle}
        size="sm"
      />
    </div>
  );
};
