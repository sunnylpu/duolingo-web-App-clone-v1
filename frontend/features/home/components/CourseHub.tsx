"use client";

import React from "react";
import Link from "next/link";
import { CourseSummary } from "@/types";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";

const COURSE_FLAGS: Record<string, string> = {
  crs_english: "🇬🇧",
  crs_spanish: "🇪🇸",
  crs_french: "🇫🇷",
  en: "🇬🇧",
  es: "🇪🇸",
  fr: "🇫🇷",
};

interface CourseHubProps {
  courses: CourseSummary[];
  currentCourseId?: string;
  onSelectCourse?: (courseId: string) => void;
}

export const CourseHub: React.FC<CourseHubProps> = ({
  courses,
  currentCourseId,
  onSelectCourse,
}) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span>📚</span>
          <span>Course Hub</span>
        </h2>
        <span className="text-xs text-gray-400 font-bold">
          {courses.length} Available Courses
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {courses.map((c) => {
          const flag = COURSE_FLAGS[c.id] || COURSE_FLAGS[c.code] || "🌐";
          const pct = c.progress_percent ?? 0;
          const isSelected = c.id === currentCourseId;
          const totalSkills = c.total_skills || (c.code === "en" ? 32 : c.code === "es" ? 20 : 14);
          const completedSkills = c.completed_skills || 0;

          return (
            <Card
              key={c.id}
              className={`p-4 bg-[#182830] border-2 transition-all flex flex-col justify-between gap-3 ${
                isSelected
                  ? "border-[#58cc02] shadow-lg shadow-[#58cc02]/10"
                  : "border-[#37464f] hover:border-gray-500"
              }`}
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <span className="text-2xl">{flag}</span>
                    <span className="text-base font-black text-white">{c.name}</span>
                  </div>
                  <span className="text-xs font-black text-[#58cc02]">{pct}%</span>
                </div>

                <div className="text-xs text-gray-400 font-bold">
                  {completedSkills} / {totalSkills} skills mastered
                </div>

                <ProgressBar value={pct} height="h-2" color="bg-[#58cc02]" />
              </div>

              <div className="pt-1">
                {onSelectCourse ? (
                  <button
                    onClick={() => onSelectCourse(c.id)}
                    className={`w-full py-2 rounded-xl text-xs font-black tracking-wider transition-all ${
                      isSelected
                        ? "bg-[#58cc02] text-black shadow-[0_2px_0_#46a302]"
                        : "bg-[#131f24] hover:bg-[#1899d6]/20 border border-[#37464f] text-white hover:text-[#1cb0f6]"
                    }`}
                  >
                    {isSelected ? "ACTIVE COURSE" : pct > 0 ? "SWITCH & CONTINUE" : "START COURSE"}
                  </button>
                ) : (
                  <Link
                    href={`/learn?course=${c.id}`}
                    className="w-full py-2 rounded-xl bg-[#131f24] hover:bg-[#1899d6]/20 border border-[#37464f] text-xs font-black text-center text-white hover:text-[#1cb0f6] transition-all block"
                  >
                    {pct > 0 ? "CONTINUE →" : "START →"}
                  </Link>
                )}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
