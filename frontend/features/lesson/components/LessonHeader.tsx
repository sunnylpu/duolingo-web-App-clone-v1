import React from "react";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { UserStats } from "@/types";

interface LessonHeaderProps {
  currentIndex: number;
  totalExercises: number;
  stats?: UserStats | null;
  onExit: () => void;
}

export const LessonHeader: React.FC<LessonHeaderProps> = ({
  currentIndex,
  totalExercises,
  stats,
  onExit,
}) => {
  const percentage =
    totalExercises > 0
      ? Math.round(((currentIndex + 1) / totalExercises) * 100)
      : 0;

  return (
    <header className="sticky top-0 z-30 bg-[#131f24] border-b border-[#37464f] px-4 py-3">
      <div className="max-w-2xl mx-auto flex items-center gap-4">
        {/* Exit Button */}
        <button
          onClick={onExit}
          className="text-gray-400 hover:text-white font-black text-2xl px-2 py-1 transition-colors leading-none"
          aria-label="Exit lesson"
        >
          ×
        </button>

        {/* Progress Bar & Counter */}
        <div className="flex-1 space-y-1">
          <ProgressBar value={percentage} height="h-3" color="bg-[#58cc02]" />
        </div>

        {/* Hearts Display (Display-only) */}
        <div className="flex items-center gap-1.5 px-3 py-1 bg-[#182830] border border-[#ff4b4b]/30 rounded-xl text-[#ff4b4b] font-black text-sm">
          <span>❤️</span>
          <span>{stats ? stats.hearts : 5}</span>
        </div>
      </div>
    </header>
  );
};
