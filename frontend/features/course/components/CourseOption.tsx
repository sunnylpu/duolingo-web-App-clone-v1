"use client";

import React from "react";
import { CourseSummary } from "@/types";
import { CourseProgressBadge } from "./CourseProgressBadge";

const COURSE_FLAGS: Record<string, string> = {
  crs_english: "🇬🇧",
  crs_spanish: "🇪🇸",
  crs_french: "🇫🇷",
  en: "🇬🇧",
  es: "🇪🇸",
  fr: "🇫🇷",
};

interface CourseOptionProps {
  course: CourseSummary;
  isSelected: boolean;
  onSelect: (courseId: string) => void;
}

export const CourseOption: React.FC<CourseOptionProps> = ({
  course,
  isSelected,
  onSelect,
}) => {
  const flag = COURSE_FLAGS[course.id] || COURSE_FLAGS[course.code] || "🌐";
  const progressPercent = course.progress_percent ?? 0;

  return (
    <button
      onClick={() => onSelect(course.id)}
      className={`w-full text-left p-3 rounded-xl transition-all duration-200 flex flex-col gap-2 border ${
        isSelected
          ? "bg-slate-800/90 border-emerald-500/50 shadow-md shadow-emerald-500/10"
          : "bg-slate-900/60 border-slate-700/50 hover:bg-slate-800/50 hover:border-slate-600"
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="text-2xl" role="img" aria-label={course.name}>
            {flag}
          </span>
          <span className={`font-bold text-sm ${isSelected ? "text-emerald-400" : "text-white"}`}>
            {course.name}
          </span>
        </div>
        {isSelected && (
          <span className="px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            Active
          </span>
        )}
      </div>

      <CourseProgressBadge
        progressPercent={progressPercent}
        completedSkills={course.completed_skills}
        totalSkills={course.total_skills}
      />
    </button>
  );
};
