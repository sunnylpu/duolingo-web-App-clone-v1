import { apiClient } from "@/lib/api-client";
import { PathResponse } from "@/types";

export const pathService = {
  getLearningPath: (courseId?: string): Promise<PathResponse> => {
    const query = courseId ? `?course_id=${encodeURIComponent(courseId)}` : "";
    return apiClient.get<PathResponse>(`/path${query}`);
  },
};
