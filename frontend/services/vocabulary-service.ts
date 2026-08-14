import { apiClient } from "@/lib/api-client";

export interface VocabularyItem {
  id: string;
  word: string;
  translation: string;
  topic: string;
  difficulty: number;
  course_id: string;
  course_name: string;
  skill_title?: string | null;
  phonetic?: string | null;
}

export interface VocabularyResponse {
  course_id: string;
  total_items: number;
  topics: string[];
  items: VocabularyItem[];
}

export const vocabularyService = {
  getVocabulary: (
    courseId?: string,
    topic?: string,
    difficulty?: number,
    query?: string
  ): Promise<VocabularyResponse> => {
    const params = new URLSearchParams();
    if (courseId) params.append("course_id", courseId);
    if (topic && topic.toLowerCase() !== "all") params.append("topic", topic);
    if (difficulty) params.append("difficulty", String(difficulty));
    if (query) params.append("q", query);
    const queryStr = params.toString() ? `?${params.toString()}` : "";
    return apiClient.get<VocabularyResponse>(`/vocabulary${queryStr}`);
  },
};
