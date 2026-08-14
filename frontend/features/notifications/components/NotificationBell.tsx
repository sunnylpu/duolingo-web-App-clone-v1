"use client";

import React, { useState, useRef, useEffect } from "react";
import { useNotifications } from "../hooks/useNotifications";
import { NotificationPanel } from "./NotificationPanel";

export const NotificationBell: React.FC = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const { data, loading, markAsRead, markAllAsRead } = useNotifications();
  const dropdownRef = useRef<HTMLDivElement>(null);

  const unreadCount = data?.unread_count || 0;

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        aria-label={`${unreadCount} unread notifications`}
        className="relative p-2 rounded-xl bg-[#182830] hover:bg-[#203038] border-2 border-[#37464f] hover:border-[#1cb0f6] text-white transition-all flex items-center justify-center"
      >
        <span className="text-lg">🔔</span>
        {unreadCount > 0 && (
          <span className="absolute -top-1.5 -right-1.5 bg-[#ff4b4b] text-white text-[10px] font-black px-1.5 py-0.5 rounded-full border-2 border-[#131f24] animate-pulse">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 z-50">
          <NotificationPanel
            data={data}
            loading={loading}
            onMarkRead={markAsRead}
            onMarkAllRead={markAllAsRead}
            onClose={() => setIsOpen(false)}
          />
        </div>
      )}
    </div>
  );
};
