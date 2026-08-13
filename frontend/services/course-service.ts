import { apiClient } from "@/lib/api-client";
import { CourseSummary, CourseDetail } from "@/types";

export const courseService = {
  getCourses: (): Promise<CourseSummary[]> => apiClient.get<CourseSummary[]>("/courses"),
  getCourse: (courseId: string): Promise<CourseDetail> => apiClient.get<CourseDetail>(`/courses/${courseId}`),
};
