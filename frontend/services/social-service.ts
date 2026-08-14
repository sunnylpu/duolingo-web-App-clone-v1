import { apiClient } from "@/lib/api-client";

export interface UserSocialSummary {
  id: string;
  username: string;
  display_name: string;
  avatar: string;
  total_xp: number;
  current_streak: number;
  is_following: boolean;
}

export interface SocialStats {
  followers_count: number;
  following_count: number;
}

export interface ActivityEvent {
  id: string;
  user: UserSocialSummary;
  event_type: string;
  message: string;
  metadata?: Record<string, any> | null;
  created_at: string;
}

export interface ActivityFeedResponse {
  items: ActivityEvent[];
  total: number;
}

export interface PublicProfile {
  id: string;
  username: string;
  display_name: string;
  avatar: string;
  total_xp: number;
  current_streak: number;
  longest_streak: number;
  followers_count: number;
  following_count: number;
  is_following: boolean;
}

export interface FriendSuggestion {
  user: UserSocialSummary;
  reason: string;
}

export const socialService = {
  getSocialStats: (): Promise<SocialStats> => {
    return apiClient.get<SocialStats>("/social/me");
  },
  getFollowing: (): Promise<UserSocialSummary[]> => {
    return apiClient.get<UserSocialSummary[]>("/social/following");
  },
  getFollowers: (): Promise<UserSocialSummary[]> => {
    return apiClient.get<UserSocialSummary[]>("/social/followers");
  },
  getSuggestions: (): Promise<FriendSuggestion[]> => {
    return apiClient.get<FriendSuggestion[]>("/social/suggestions");
  },
  getFeed: (limit = 20, offset = 0): Promise<ActivityFeedResponse> => {
    return apiClient.get<ActivityFeedResponse>(`/social/feed?limit=${limit}&offset=${offset}`);
  },
  getPublicProfile: (userId: string): Promise<PublicProfile> => {
    return apiClient.get<PublicProfile>(`/social/users/${userId}`);
  },
  followUser: (userId: string): Promise<{ status: string; user_id: string }> => {
    return apiClient.post<{ status: string; user_id: string }>(`/social/users/${userId}/follow`, {});
  },
  unfollowUser: (userId: string): Promise<{ status: string; user_id: string }> => {
    return apiClient.delete<{ status: string; user_id: string }>(`/social/users/${userId}/follow`);
  },
};
