"use client";

import React from "react";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface CourseCompleteProps {
  courseName: string;
  courseBonusXp?: number;
  totalUnits?: number;
  totalSkills?: number;
  totalLessons?: number;
  onContinue: () => void;
}

export const CourseComplete: React.FC<CourseCompleteProps> = ({
  courseName,
  courseBonusXp = 500,
  totalUnits = 8,
  totalSkills = 32,
  totalLessons = 96,
  onContinue,
}) => {
  return (
    <div className="max-w-md mx-auto py-12 px-4 text-center animate-fadeIn select-none">
      <Card className="p-8 space-y-6 bg-[#182830] border-4 border-[#ffc800] shadow-2xl shadow-[#ffc800]/20">
        <div className="w-24 h-24 rounded-full bg-[#ffc800]/20 border-4 border-[#ffc800] text-[#ffc800] flex items-center justify-center text-5xl mx-auto motion-safe:animate-bounce">
          🎓
        </div>

        <div>
          <h2 className="text-3xl font-black text-[#ffc800] tracking-wide uppercase">
            COURSE MASTERED!
          </h2>
          <p className="text-sm font-extrabold text-white mt-1">
            You have mastered {courseName}!
          </p>
        </div>

        <div className="p-4 bg-[#ffc800]/20 border-2 border-[#ffc800] rounded-2xl space-y-1 text-center animate-pulse">
          <div className="text-3xl">🏆</div>
          <div className="text-xs font-black uppercase text-[#ffc800] tracking-wider">
            TOP-LEVEL MASTERY BONUS (+{courseBonusXp} XP)
          </div>
          <div className="text-base font-extrabold text-white">
            {courseName} Master Badge Unlocked
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3 py-1 text-center">
          <div className="p-3 bg-[#131f24] rounded-2xl border border-[#37464f]">
            <div className="text-[10px] text-gray-400 font-bold uppercase">Units</div>
            <div className="text-lg font-black text-white mt-0.5">{totalUnits} / {totalUnits}</div>
          </div>
          <div className="p-3 bg-[#131f24] rounded-2xl border border-[#37464f]">
            <div className="text-[10px] text-gray-400 font-bold uppercase">Skills</div>
            <div className="text-lg font-black text-[#58cc02] mt-0.5">{totalSkills} / {totalSkills}</div>
          </div>
          <div className="p-3 bg-[#131f24] rounded-2xl border border-[#37464f]">
            <div className="text-[10px] text-gray-400 font-bold uppercase">Lessons</div>
            <div className="text-lg font-black text-[#1cb0f6] mt-0.5">{totalLessons} / {totalLessons}</div>
          </div>
        </div>

        <Button
          variant="primary"
          size="lg"
          className="w-full py-4 text-base font-black tracking-wider shadow-[0_4px_0_#1899d6]"
          onClick={onContinue}
        >
          CLAIM MASTERY →
        </Button>
      </Card>
    </div>
  );
};
