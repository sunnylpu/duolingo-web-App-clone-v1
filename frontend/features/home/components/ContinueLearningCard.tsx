"use client";

import React from "react";
import Link from "next/link";
import { ContinueLearningSummary } from "@/services/home-service";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";

interface ContinueLearningCardProps {
  summary: ContinueLearningSummary;
  courseName: string;
}

export const ContinueLearningCard: React.FC<ContinueLearningCardProps> = ({
  summary,
  courseName,
}) => {
  const {
    unit_title,
    skill_title,
    lesson_id,
    lesson_title,
    progress_percent = 0,
    lessons_completed = 0,
    total_lessons = 3,
  } = summary;

  const pct = Math.round(progress_percent);
  const href = lesson_id ? `/lesson/${lesson_id}` : "/learn";

  return (
    <Card className="p-6 bg-[#182830] border-2 border-[#58cc02] shadow-xl relative overflow-hidden group">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div className="space-y-2 flex-1">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-0.5 text-[10px] font-black uppercase tracking-wider rounded-full bg-[#58cc02]/20 text-[#58cc02] border border-[#58cc02]/30">
              Continue Learning
            </span>
            {unit_title && (
              <span className="text-xs font-bold text-gray-400">
                {unit_title}
              </span>
            )}
          </div>

          <h2 className="text-2xl sm:text-3xl font-black text-white group-hover:text-[#58cc02] transition-colors">
            {skill_title || `${courseName} Foundations`}
          </h2>

          {lesson_title && (
            <p className="text-xs sm:text-sm text-gray-300 font-medium flex items-center gap-2">
              <span>Next Lesson:</span>
              <span className="font-extrabold text-white">{lesson_title}</span>
              <span className="text-gray-500">({lessons_completed}/{total_lessons} completed)</span>
            </p>
          )}

          <div className="w-full max-w-md pt-2 space-y-1">
            <div className="flex justify-between text-xs font-bold text-gray-400">
              <span>Skill Mastery</span>
              <span className="text-[#58cc02] font-extrabold">{pct}%</span>
            </div>
            <ProgressBar value={pct} height="h-3" color="bg-[#58cc02]" />
          </div>
        </div>

        <Link
          href={href}
          className="w-full sm:w-auto px-8 py-4 rounded-2xl bg-[#58cc02] hover:bg-[#61e002] text-black font-black text-base text-center tracking-wider shadow-[0_4px_0_#46a302] active:translate-y-1 transition-all shrink-0 flex items-center justify-center gap-2"
        >
          <span>CONTINUE LEARNING</span>
          <span className="text-xl">→</span>
        </Link>
      </div>
    </Card>
  );
};
