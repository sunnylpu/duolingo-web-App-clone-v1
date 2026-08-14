"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { NotificationItem as NotificationItemType } from "@/services/notification-service";

interface NotificationItemProps {
  item: NotificationItemType;
  onMarkRead: (id: string) => void;
}

const NOTIF_ICONS: Record<string, string> = {
  DAILY_REMINDER: "🔔",
  STREAK_REMINDER: "🔥",
  QUEST_REMINDER: "🎯",
  ACHIEVEMENT_UNLOCKED: "🏆",
  UNIT_COMPLETED: "🎉",
  COURSE_COMPLETED: "🎓",
  SOCIAL_ACTIVITY: "👥",
};

export const NotificationItem: React.FC<NotificationItemProps> = ({ item, onMarkRead }) => {
  const router = useRouter();
  const icon = NOTIF_ICONS[item.type] || "🔔";

  const handleClick = () => {
    if (!item.is_read) {
      onMarkRead(item.id);
    }

    // Deep-link navigation logic based on notification metadata
    if (item.metadata?.course_id) {
      router.push(`/learn?course=${item.metadata.course_id}`);
    } else if (item.metadata?.achievement_id) {
      router.push("/profile");
    } else if (item.metadata?.user_id) {
      router.push(`/profile/${item.metadata.user_id}`);
    } else if (item.type === "QUEST_REMINDER" || item.type === "DAILY_REMINDER" || item.type === "STREAK_REMINDER") {
      router.push("/learn");
    }
  };

  const formattedTime = new Date(item.created_at).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div
      onClick={handleClick}
      className={`p-3.5 rounded-2xl border transition-all cursor-pointer flex items-start gap-3 ${
        item.is_read
          ? "bg-[#131f24]/60 border-[#37464f]/50 opacity-80 hover:opacity-100"
          : "bg-[#182830] border-[#1cb0f6]/50 shadow-md hover:border-[#1cb0f6]"
      }`}
    >
      <div className="w-10 h-10 rounded-xl bg-[#131f24] border border-[#37464f] flex items-center justify-center text-xl shrink-0">
        {icon}
      </div>

      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between gap-2">
          <h4
            className={`text-xs font-black truncate ${
              item.is_read ? "text-gray-300" : "text-white"
            }`}
          >
            {item.title}
          </h4>
          <span className="text-[10px] text-gray-400 font-bold shrink-0">{formattedTime}</span>
        </div>
        <p className="text-[11px] text-gray-400 font-medium mt-0.5 line-clamp-2">
          {item.message}
        </p>
      </div>

      {!item.is_read && (
        <span className="w-2.5 h-2.5 rounded-full bg-[#1cb0f6] shrink-0 mt-1" aria-label="Unread" />
      )}
    </div>
  );
};
