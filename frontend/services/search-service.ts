import { apiClient } from "@/lib/api-client";

export interface SearchResultItem {
  id: string;
  type: "course" | "unit" | "skill" | "lesson" | "vocabulary";
  title: string;
  description?: string | null;
  course_id?: string | null;
  course_name?: string | null;
  unit_id?: string | null;
  skill_id?: string | null;
  status?: string | null;
  progress_percent?: number | null;
}

export interface SearchResponse {
  query: string;
  total_results: number;
  results: SearchResultItem[];
}

export const searchService = {
  search: (query: string, courseId?: string, type?: string): Promise<SearchResponse> => {
    const params = new URLSearchParams({ q: query });
    if (courseId) params.append("course_id", courseId);
    if (type) params.append("type", type);
    return apiClient.get<SearchResponse>(`/search?${params.toString()}`);
  },
};
