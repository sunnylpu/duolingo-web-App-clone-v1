import React from "react";
import { UserStats } from "@/types";
import { HeartDisplay } from "@/components/gamification/HeartDisplay";

interface LessonHeaderProps {
  currentIndex: number;
  totalExercises: number;
  stats?: UserStats | null;
  heartsOverride?: number | null;
  onExit: () => void;
}

export const LessonHeader: React.FC<LessonHeaderProps> = ({
  currentIndex,
  totalExercises,
  stats,
  heartsOverride = null,
  onExit,
}) => {
  const progressPercent = totalExercises > 0 ? (currentIndex / totalExercises) * 100 : 0;
  const currentHearts = heartsOverride !== null ? heartsOverride : stats?.hearts ?? 5;

  return (
    <header className="fixed top-0 left-0 right-0 z-30 bg-[#131f24] border-b border-[#37464f]/40 px-4 py-3">
      <div className="max-w-3xl mx-auto flex items-center justify-between gap-4">
        {/* Exit Button (×) */}
        <button
          type="button"
          onClick={onExit}
          className="text-gray-400 hover:text-white font-black text-2xl w-8 h-8 flex items-center justify-center rounded-lg hover:bg-[#182830] transition-colors"
          aria-label="Exit lesson"
        >
          ✕
        </button>

        {/* Progress Bar Container */}
        <div className="flex-1 h-3.5 bg-[#182830] rounded-full overflow-hidden border border-[#37464f] p-0.5">
          <div
            className="h-full bg-[#58cc02] rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Hearts Display Component */}
        <HeartDisplay hearts={currentHearts} maxHearts={5} />
      </div>
    </header>
  );
};
