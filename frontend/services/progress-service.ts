import { apiClient } from "@/lib/api-client";
import { ProgressResponse } from "@/types";

export const progressService = {
  getProgress: (): Promise<ProgressResponse> => apiClient.get<ProgressResponse>("/progress"),
};
