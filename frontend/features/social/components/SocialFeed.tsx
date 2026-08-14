"use client";

import React from "react";
import Link from "next/link";
import { ActivityEvent } from "@/services/social-service";

interface SocialFeedProps {
  items: ActivityEvent[];
  loading?: boolean;
}

const EVENT_ICONS: Record<string, string> = {
  streak_milestone: "🔥",
  achievement_earned: "🏆",
  unit_completed: "👑",
  course_completed: "🎓",
  lesson_completed: "⚡",
  skill_completed: "🔮",
};

export const SocialFeed: React.FC<SocialFeedProps> = ({ items, loading }) => {
  if (loading) {
    return (
      <div className="py-8 text-center text-xs font-black text-gray-400 animate-pulse">
        Loading social activity feed...
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="p-6 bg-[#182830] border-2 border-[#37464f] rounded-2xl text-center space-y-2">
        <span className="text-3xl">👥</span>
        <h4 className="text-sm font-black text-white">No Recent Activity</h4>
        <p className="text-xs text-gray-400 max-w-xs mx-auto">
          Follow other learners to see their lesson completions, streak milestones, and achievements here!
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item) => {
        const icon = EVENT_ICONS[item.event_type] || "⭐";
        const dateStr = new Date(item.created_at).toLocaleDateString(undefined, {
          month: "short",
          day: "numeric",
        });

        return (
          <div
            key={item.id}
            className="p-4 bg-[#182830] border-2 border-[#37464f] rounded-2xl flex items-start gap-3.5"
          >
            <div className="w-10 h-10 rounded-full bg-[#131f24] border border-[#37464f] flex items-center justify-center text-xl shrink-0">
              {icon}
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <Link
                  href={`/profile/${item.user.id}`}
                  className="text-xs font-black text-white hover:text-[#1cb0f6] transition-colors truncate"
                >
                  {item.user.display_name}
                </Link>
                <span className="text-[10px] font-bold text-gray-500">{dateStr}</span>
              </div>
              <p className="text-xs text-gray-300 font-medium mt-0.5 leading-relaxed">
                {item.message}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
};
