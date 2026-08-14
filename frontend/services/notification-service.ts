import { apiClient } from "@/lib/api-client";

export interface NotificationItem {
  id: string;
  user_id: string;
  type: string;
  title: string;
  message: string;
  metadata?: Record<string, any> | null;
  is_read: boolean;
  created_at: string;
}

export interface NotificationListResponse {
  items: NotificationItem[];
  unread_count: number;
  total: number;
}

export interface NotificationPreferences {
  user_id: string;
  daily_reminders: boolean;
  streak_reminders: boolean;
  quest_reminders: boolean;
  social_notifications: boolean;
  achievement_notifications: boolean;
}

export interface NotificationPreferenceUpdate {
  daily_reminders?: boolean;
  streak_reminders?: boolean;
  quest_reminders?: boolean;
  social_notifications?: boolean;
  achievement_notifications?: boolean;
}

export const notificationService = {
  getNotifications: (unreadOnly = false, limit = 20, offset = 0): Promise<NotificationListResponse> => {
    const params = new URLSearchParams();
    if (unreadOnly) params.set("unread_only", "true");
    params.set("limit", limit.toString());
    params.set("offset", offset.toString());
    return apiClient.get<NotificationListResponse>(`/notifications?${params.toString()}`);
  },

  markAsRead: (id: string): Promise<{ status: string }> => {
    return apiClient.post<{ status: string }>(`/notifications/${id}/read`);
  },

  markAllAsRead: (): Promise<{ status: string; marked_read_count: number }> => {
    return apiClient.post<{ status: string; marked_read_count: number }>("/notifications/read-all");
  },

  getPreferences: (): Promise<NotificationPreferences> => {
    return apiClient.get<NotificationPreferences>("/notifications/preferences");
  },

  updatePreferences: (payload: NotificationPreferenceUpdate): Promise<NotificationPreferences> => {
    return apiClient.patch<NotificationPreferences>("/notifications/preferences", payload);
  },
};
