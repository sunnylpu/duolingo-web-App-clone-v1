import { apiClient } from "@/lib/api-client";

export interface QuestItem {
  id: string;
  code: string;
  title: string;
  description: string;
  quest_type: string;
  quest_scope: "daily" | "weekly";
  current_value: number;
  target_value: number;
  reward_xp: number;
  completed: boolean;
  completed_at?: string | null;
  course_id?: string | null;
}

export interface DailyQuestsResponse {
  date: string;
  user_id: string;
  quests: QuestItem[];
}

export interface WeeklyChallengeResponse {
  week_start_date: string;
  challenge?: QuestItem | null;
}

export interface QuestHistoryResponse {
  total_completed: number;
  quests: QuestItem[];
}

export const questService = {
  getTodayQuests: (): Promise<DailyQuestsResponse> => {
    return apiClient.get<DailyQuestsResponse>("/quests/today");
  },
  getWeeklyChallenge: (): Promise<WeeklyChallengeResponse> => {
    return apiClient.get<WeeklyChallengeResponse>("/quests/weekly");
  },
  getHistory: (limit = 20): Promise<QuestHistoryResponse> => {
    return apiClient.get<QuestHistoryResponse>(`/quests/history?limit=${limit}`);
  },
};
