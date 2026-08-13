import React from "react";
import { CourseSummary } from "@/types";
import { Badge } from "@/components/ui/Badge";

interface CourseHeaderProps {
  course: CourseSummary;
  totalUnits: number;
}

export const CourseHeader: React.FC<CourseHeaderProps> = ({
  course,
  totalUnits,
}) => {
  return (
    <div className="duo-card p-6 bg-gradient-to-r from-[#182830] to-[#131f24] border-2 border-[#1cb0f6] mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Badge variant="blue">Language Course</Badge>
            <span className="text-xs font-bold text-gray-400">
              {course.source_language.toUpperCase()} → {course.target_language.toUpperCase()}
            </span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
            {course.name}
          </h1>
          {course.description && (
            <p className="text-xs sm:text-sm text-gray-400 mt-1 max-w-xl">
              {course.description}
            </p>
          )}
        </div>

        <div className="flex items-center gap-3 self-start sm:self-center">
          <div className="bg-[#131f24] px-4 py-2 rounded-2xl border border-[#37464f] text-center">
            <div className="text-xs text-gray-400 font-bold uppercase">Units</div>
            <div className="text-lg font-black text-[#1cb0f6]">{totalUnits}</div>
          </div>
        </div>
      </div>
    </div>
  );
};
