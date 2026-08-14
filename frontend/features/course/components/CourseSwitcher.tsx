"use client";

import React, { useState, useEffect, useRef } from "react";
import { usePathname } from "next/navigation";
import { courseService } from "@/services/course-service";
import { CourseSummary } from "@/types";
import { useCurrentCourse } from "../hooks/useCurrentCourse";
import { CourseOption } from "./CourseOption";

const COURSE_FLAGS: Record<string, string> = {
  crs_english: "🇬🇧",
  crs_spanish: "🇪🇸",
  crs_french: "🇫🇷",
  en: "🇬🇧",
  es: "🇪🇸",
  fr: "🇫🇷",
};

export const CourseSwitcher: React.FC = () => {
  const pathname = usePathname();
  const { currentCourseId, selectCourse } = useCurrentCourse();
  const [courses, setCourses] = useState<CourseSummary[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Hide switcher inside active lesson route to prevent abandoning lesson session
  const isInsideLesson = pathname?.startsWith("/lesson");

  useEffect(() => {
    let isMounted = true;
    async function loadCourses() {
      try {
        const data = await courseService.getCourses();
        if (isMounted) {
          setCourses(data);
          setIsLoading(false);
        }
      } catch (err) {
        console.error("Failed to load courses for switcher:", err);
        if (isMounted) setIsLoading(false);
      }
    }
    loadCourses();
    return () => {
      isMounted = false;
    };
  }, [currentCourseId]);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  if (isInsideLesson) {
    return null;
  }

  const selectedCourse = courses.find((c) => c.id === currentCourseId) || {
    id: currentCourseId,
    name: currentCourseId === "crs_spanish" ? "Spanish" : currentCourseId === "crs_french" ? "French" : "English",
    code: currentCourseId === "crs_spanish" ? "es" : currentCourseId === "crs_french" ? "fr" : "en",
    source_language: "en",
    target_language: "en",
    description: "",
    is_active: true,
  };

  const flag = COURSE_FLAGS[selectedCourse.id] || COURSE_FLAGS[selectedCourse.code] || "🌐";

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        disabled={isLoading}
        className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/60 text-white font-bold text-sm transition-all duration-200 shadow-sm active:scale-95 disabled:opacity-50"
        aria-expanded={isOpen}
        aria-label="Select course"
      >
        <span className="text-lg" role="img" aria-label={selectedCourse.name}>
          {flag}
        </span>
        <span className="hidden sm:inline-block text-slate-100">{selectedCourse.name}</span>
        <svg
          className={`w-4 h-4 text-slate-400 transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-64 bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl p-3 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
          <div className="text-xs font-extrabold uppercase tracking-wider text-slate-400 mb-2 px-1">
            My Courses
          </div>
          <div className="flex flex-col gap-2 max-h-80 overflow-y-auto">
            {courses.length > 0 ? (
              courses.map((course) => (
                <CourseOption
                  key={course.id}
                  course={course}
                  isSelected={course.id === currentCourseId}
                  onSelect={(id) => {
                    selectCourse(id);
                    setIsOpen(false);
                  }}
                />
              ))
            ) : (
              <div className="text-xs text-slate-400 p-2 text-center">Loading courses...</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
