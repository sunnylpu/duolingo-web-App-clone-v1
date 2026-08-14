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

interface CourseProgressCardProps {
  course: CourseSummary;
}

export const CourseProgressCard: React.FC<CourseProgressCardProps> = ({ course }) => {
  const flag = COURSE_FLAGS[course.id] || COURSE_FLAGS[course.code] || "🌐";
  const pct = course.progress_percent ?? 0;
  const isCompleted = course.status === "completed" || pct >= 100;

  const totalUnits = course.total_units || (course.code === "en" ? 8 : course.code === "es" ? 5 : 3);
  const completedUnits = course.completed_units || 0;
  const totalSkills = course.total_skills || (course.code === "en" ? 32 : course.code === "es" ? 20 : 14);
  const completedSkills = course.completed_skills || 0;
  const totalLessons = course.total_lessons || (course.code === "en" ? 96 : course.code === "es" ? 60 : 42);
  const completedLessons = course.completed_lessons || 0;

  return (
    <Card className="p-5 bg-[#182830] border-2 border-[#37464f] hover:border-[#58cc02] transition-all group flex flex-col justify-between gap-4">
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="text-3xl" role="img" aria-label={course.name}>
              {flag}
            </span>
            <div>
              <h3 className="text-lg font-black text-white group-hover:text-[#58cc02] transition-colors">
                {course.name}
              </h3>
              <p className="text-xs text-gray-400 font-medium capitalize">
                {course.source_language} → {course.target_language}
              </p>
            </div>
          </div>
          {isCompleted ? (
            <span className="px-2.5 py-1 text-xs font-black uppercase tracking-wider rounded-full bg-[#ffc800]/20 text-[#ffc800] border border-[#ffc800]/30 flex items-center gap-1">
              <span>🎓</span> Mastered
            </span>
          ) : (
            <span className="text-xs font-black text-[#58cc02]">{pct}%</span>
          )}
        </div>

        <div className="grid grid-cols-3 gap-2 text-center text-xs font-bold py-1">
          <div className="p-2 bg-[#131f24] rounded-xl border border-[#37464f]">
            <div className="text-gray-400 text-[10px] uppercase">Units</div>
            <div className="text-white font-extrabold mt-0.5">{completedUnits} / {totalUnits}</div>
          </div>
          <div className="p-2 bg-[#131f24] rounded-xl border border-[#37464f]">
            <div className="text-gray-400 text-[10px] uppercase">Skills</div>
            <div className="text-[#58cc02] font-extrabold mt-0.5">{completedSkills} / {totalSkills}</div>
          </div>
          <div className="p-2 bg-[#131f24] rounded-xl border border-[#37464f]">
            <div className="text-gray-400 text-[10px] uppercase">Lessons</div>
            <div className="text-[#1cb0f6] font-extrabold mt-0.5">{completedLessons} / {totalLessons}</div>
          </div>
        </div>

        <ProgressBar value={pct} height="h-2.5" />
      </div>

      <Link
        href={`/learn?course=${course.id}`}
        className="w-full py-2.5 rounded-xl bg-[#131f24] hover:bg-[#1899d6]/20 border border-[#37464f] hover:border-[#1cb0f6] text-xs font-black text-center text-white hover:text-[#1cb0f6] transition-all block"
      >
        {isCompleted ? "REVIEW COURSE →" : "CONTINUE LEARNING →"}
      </Link>
    </Card>
  );
};
