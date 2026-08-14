"use client";

import React from "react";
import { NotificationListResponse } from "@/services/notification-service";
import { NotificationItem } from "./NotificationItem";

interface NotificationPanelProps {
  data: NotificationListResponse | null;
  loading: boolean;
  onMarkRead: (id: string) => void;
  onMarkAllRead: () => void;
  onClose?: () => void;
}

export const NotificationPanel: React.FC<NotificationPanelProps> = ({
  data,
  loading,
  onMarkRead,
  onMarkAllRead,
  onClose,
}) => {
  return (
    <div className="w-80 sm:w-96 bg-[#182830] border-2 border-[#37464f] rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[480px] z-50">
      {/* Header */}
      <div className="p-4 border-b border-[#37464f] flex items-center justify-between bg-[#131f24]">
        <div className="flex items-center gap-2">
          <h3 className="text-sm font-black text-white uppercase tracking-wider">
            Notifications
          </h3>
          {data && data.unread_count > 0 && (
            <span className="text-[10px] font-black text-white bg-[#ff4b4b] px-2 py-0.5 rounded-full">
              {data.unread_count} new
            </span>
          )}
        </div>

        {data && data.unread_count > 0 && (
          <button
            onClick={onMarkAllRead}
            className="text-xs font-black text-[#1cb0f6] hover:text-[#1cb0f6]/80 transition-all"
          >
            Mark all read
          </button>
        )}
      </div>

      {/* Content */}
      <div className="p-3 overflow-y-auto space-y-2 flex-1 scrollbar-thin scrollbar-thumb-[#37464f]">
        {loading ? (
          <div className="p-6 text-center text-xs text-gray-400 font-bold space-y-2 animate-pulse">
            <div className="h-12 bg-[#131f24] rounded-xl" />
            <div className="h-12 bg-[#131f24] rounded-xl" />
          </div>
        ) : !data || data.items.length === 0 ? (
          <div className="p-8 text-center space-y-2">
            <div className="text-3xl">🔔</div>
            <p className="text-xs font-black text-white">No notifications yet</p>
            <p className="text-[11px] text-gray-400 font-medium">
              We&apos;ll notify you about streak reminders, quest updates, and achievements here.
            </p>
          </div>
        ) : (
          data.items.map((item) => (
            <NotificationItem key={item.id} item={item} onMarkRead={onMarkRead} />
          ))
        )}
      </div>
    </div>
  );
};
