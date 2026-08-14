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
  const unitBonusXp = result?.unit_bonus_xp ?? 0;
  const courseBonusXp = result?.course_bonus_xp ?? 0;
  const totalXpAwarded = xpEarned + unitBonusXp + courseBonusXp;
  const score = result?.score ?? 100;
  const progressPercent = Math.round(result?.skill_progress?.completion_percent ?? 100);
  const crownLevel = result?.skill_progress?.crown_level ?? 1;

  const currentStreak = result?.streak?.current ?? 1;
  const streakIncreased = result?.streak?.increased ?? false;
  const dailyXp = result?.daily_progress?.xp ?? totalXpAwarded;
  const dailyGoalXp = result?.daily_progress?.goal ?? 30;
  const goalJustCompleted = result?.daily_progress?.goal_just_completed ?? false;

  const unitCompleted = result?.unit_completed ?? false;
  const courseCompleted = result?.course_completed ?? false;
  const unitTitle = result?.unit?.title || "Unit Milestone";
  const courseName = result?.course?.name || "Course";

  const newlyEarnedAchievements: any[] = result?.achievements?.newly_earned ?? [];

  return (
    <div className="max-w-md mx-auto py-12 px-4 text-center animate-fadeIn select-none">
      <Card className="p-8 space-y-6 bg-[#182830] border-2 border-[#58cc02] shadow-2xl">
        {/* Celebration Header */}
        <div className="w-24 h-24 rounded-full bg-[#58cc02]/20 border-4 border-[#58cc02] text-[#58cc02] flex items-center justify-center text-5xl mx-auto motion-safe:animate-bounce">
          {courseCompleted ? "🎓" : "🎉"}
        </div>

        <div>
          <h2 className="text-3xl font-black text-white tracking-wide">
            {courseCompleted ? "COURSE MASTERED!" : "WELL DONE!"}
          </h2>
          <p className="text-xs text-gray-400 font-bold mt-1">
            {courseCompleted ? `You completed the entire ${courseName} course!` : "Lesson completed successfully"}
          </p>
        </div>

        {/* Top-Level Course Mastery Milestone Card */}
        {courseCompleted && (
          <div className="p-5 bg-[#ffc800]/20 border-4 border-[#ffc800] rounded-2xl space-y-1 text-center animate-pulse shadow-xl shadow-[#ffc800]/20">
            <div className="text-4xl">🎓</div>
            <div className="text-xs font-black uppercase text-[#ffc800] tracking-wider">
              TOP-LEVEL COURSE MASTERY BONUS (+{courseBonusXp || 500} XP)
            </div>
            <div className="text-lg font-extrabold text-white">
              {courseName} Master Badge Unlocked
            </div>
          </div>
        )}

        {/* Unit Completion Celebration Badge */}
        {unitCompleted && (
          <div className="p-4 bg-emerald-500/20 border-2 border-emerald-500 rounded-2xl space-y-1 text-center animate-bounce shadow-lg shadow-emerald-500/20">
            <div className="text-3xl">🏆</div>
            <div className="text-xs font-black uppercase text-emerald-400 tracking-wider">
              UNIT COMPLETE! (+{unitBonusXp || 50} XP BONUS)
            </div>
            <div className="text-base font-extrabold text-white">
              {unitTitle} Mastered
            </div>
          </div>
        )}

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

        {/* Newly Unlocked Achievements */}
        {newlyEarnedAchievements.map((ach) => (
          <div
            key={ach.code}
            className="p-4 bg-[#ffc800]/20 border-2 border-[#ffc800] rounded-2xl space-y-1 text-center animate-bounce"
          >
            <div className="text-3xl">{ach.icon || "🏆"}</div>
            <div className="text-xs font-black uppercase text-[#ffc800] tracking-wider">
              ACHIEVEMENT UNLOCKED!
            </div>
            <div className="text-base font-extrabold text-white">{ach.name}</div>
            <div className="text-xs text-gray-300">{ach.description}</div>
          </div>
        ))}

        {/* Stats Grid */}
        <div className="grid grid-cols-2 gap-3 py-1">
          <div className="p-4 bg-[#131f24] rounded-2xl border border-[#37464f]">
            <div className="text-xs text-gray-400 font-bold uppercase tracking-wider">TOTAL XP</div>
            <div className="text-2xl font-black text-[#ffc800] mt-1 flex items-center justify-center gap-1">
              <span>⭐</span>
              <span>+{totalXpAwarded}</span>
            </div>
            {(unitBonusXp > 0 || courseBonusXp > 0) && (
              <div className="text-[10px] text-emerald-400 font-bold mt-0.5">
                (Lesson +{xpEarned}{unitBonusXp > 0 ? `, Unit +${unitBonusXp}` : ""}{courseBonusXp > 0 ? `, Course +${courseBonusXp}` : ""})
              </div>
            )}
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
