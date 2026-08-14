"use client";

import { useState, useEffect, useCallback } from "react";
import {
  notificationService,
  NotificationItem,
  NotificationListResponse,
} from "@/services/notification-service";

export function useNotifications() {
  const [data, setData] = useState<NotificationListResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchNotifications = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await notificationService.getNotifications();
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load notifications.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchNotifications();
  }, [fetchNotifications]);

  const markAsRead = async (id: string) => {
    try {
      await notificationService.markAsRead(id);
      setData((prev) => {
        if (!prev) return prev;
        const updated = prev.items.map((item) =>
          item.id === id ? { ...item, is_read: true } : item
        );
        const newUnread = Math.max(0, prev.unread_count - 1);
        return { ...prev, items: updated, unread_count: newUnread };
      });
    } catch (err) {
      console.error("Failed to mark notification as read", err);
    }
  };

  const markAllAsRead = async () => {
    try {
      await notificationService.markAllAsRead();
      setData((prev) => {
        if (!prev) return prev;
        const updated = prev.items.map((item) => ({ ...item, is_read: true }));
        return { ...prev, items: updated, unread_count: 0 };
      });
    } catch (err) {
      console.error("Failed to mark all as read", err);
    }
  };

  return {
    data,
    loading,
    error,
    refresh: fetchNotifications,
    markAsRead,
    markAllAsRead,
  };
}
