"use client";

import { useSearchParams, useRouter, usePathname } from "next/navigation";
import { useCallback } from "react";

export const DEFAULT_COURSE_ID = "crs_english";

export function useCurrentCourse() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  const currentCourseId = searchParams.get("course") || DEFAULT_COURSE_ID;

  const selectCourse = useCallback(
    (courseId: string) => {
      const params = new URLSearchParams(searchParams.toString());
      params.set("course", courseId);
      // Navigate to path page with query param
      const targetPath = pathname === "/learn" ? "/learn" : "/learn";
      router.push(`${targetPath}?${params.toString()}`);
    },
    [searchParams, router, pathname]
  );

  return {
    currentCourseId,
    selectCourse,
    isDefaultCourse: currentCourseId === DEFAULT_COURSE_ID,
  };
}
