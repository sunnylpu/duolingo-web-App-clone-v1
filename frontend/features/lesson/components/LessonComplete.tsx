import React from "react";
import { LessonCompleteResult } from "../services/lesson-session-service";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface LessonCompleteProps {
  result: LessonCompleteResult | null;
  onContinue: () => void;
}

export const LessonComplete: React.FC<LessonCompleteProps> = ({
  result,
  onContinue,
}) => {
  const xpEarned = result?.xp_earned ?? 10;
  const score = result?.score ?? 100;
  const progressPercent = Math.round(result?.skill_progress?.completion_percent ?? 100);
  const crownLevel = result?.skill_progress?.crown_level ?? 1;

  const currentStreak = result?.streak?.current ?? 1;
  const streakIncreased = result?.streak?.increased ?? false;
  const dailyXp = result?.daily_progress?.xp ?? xpEarned;
  const dailyGoalXp = result?.daily_progress?.goal ?? 30;
  const goalJustCompleted = result?.daily_progress?.goal_just_completed ?? false;

  return (
    <div className="max-w-md mx-auto py-12 px-4 text-center animate-fadeIn select-none">
      <Card className="p-8 space-y-6 bg-[#182830] border-2 border-[#58cc02] shadow-2xl">
        {/* Celebration Header */}
        <div className="w-24 h-24 rounded-full bg-[#58cc02]/20 border-4 border-[#58cc02] text-[#58cc02] flex items-center justify-center text-5xl mx-auto motion-safe:animate-bounce">
          🎉
        </div>

        <div>
          <h2 className="text-3xl font-black text-white tracking-wide">WELL DONE!</h2>
          <p className="text-xs text-gray-400 font-bold mt-1">Lesson completed successfully</p>
        </div>

        {/* Milestone Toasts */}
        {streakIncreased && (
          <div className="p-3 bg-[#ff9600]/20 border border-[#ff9600] rounded-2xl flex items-center justify-center gap-2 text-sm font-black text-[#ff9600]">
            <span className="text-xl">🔥</span>
            <span>Streak extended! {currentStreak} day{currentStreak > 1 ? "s" : ""}</span>
          </div>
        )}

        {goalJustCompleted && (
          <div className="p-3 bg-[#58cc02]/20 border border-[#58cc02] rounded-2xl flex items-center justify-center gap-2 text-sm font-black text-[#58cc02]">
            <span className="text-xl">🎯</span>
            <span>Daily Goal Complete! ({dailyXp} / {dailyGoalXp} XP)</span>
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-3 py-1">
          <div className="p-4 bg-[#131f24] rounded-2xl border border-[#37464f]">
            <div className="text-xs text-gray-400 font-bold uppercase tracking-wider">TOTAL XP</div>
            <div className="text-2xl font-black text-[#ffc800] mt-1 flex items-center justify-center gap-1">
              <span>⭐</span>
              <span>+{xpEarned}</span>
            </div>
          </div>

          <div className="p-4 bg-[#131f24] rounded-2xl border border-[#37464f]">
            <div className="text-xs text-gray-400 font-bold uppercase tracking-wider">ACCURACY</div>
            <div className="text-2xl font-black text-[#1cb0f6] mt-1">
              {score}%
            </div>
          </div>
        </div>

        {/* Skill Progress & Crown Level */}
        <div className="p-4 bg-[#131f24] rounded-2xl border border-[#37464f] space-y-3 text-left">
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-300 font-bold uppercase tracking-wider">Skill Mastery</span>
            <span className="text-xs font-black text-[#ffc800] flex items-center gap-1">
              <span>👑</span> Level {crownLevel}
            </span>
          </div>

          <div className="h-3 bg-[#182830] rounded-full overflow-hidden border border-[#37464f]">
            <div
              className="h-full bg-[#58cc02] rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${progressPercent}%` }}
            />
          </div>
          <div className="text-right text-[11px] text-gray-400 font-bold">{progressPercent}% Completed</div>
        </div>

        {/* Return to Path CTA */}
        <Button
          variant="primary"
          size="lg"
          className="w-full py-4 text-base font-black tracking-wider shadow-[0_4px_0_#1899d6]"
          onClick={onContinue}
        >
          CONTINUE →
        </Button>
      </Card>
    </div>
  );
};
