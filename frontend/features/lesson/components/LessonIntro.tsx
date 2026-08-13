import React from "react";
import Link from "next/link";
import { LessonDetail, UserStats } from "@/types";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

interface LessonIntroProps {
  lesson: LessonDetail;
  stats?: UserStats | null;
  isStarting: boolean;
  onStart: () => void;
}

export const LessonIntro: React.FC<LessonIntroProps> = ({
  lesson,
  stats,
  isStarting,
  onStart,
}) => {
  return (
    <div className="max-w-md mx-auto py-8 px-4 space-y-6">
      <Link
        href="/learn"
        className="inline-flex items-center text-xs font-bold text-gray-400 hover:text-white transition-colors"
      >
        ← Back to Learning Path
      </Link>

      <Card className="p-8 text-center space-y-6 bg-[#182830] border-2 border-[#1cb0f6] shadow-2xl">
        <div className="w-20 h-20 rounded-3xl bg-[#1cb0f6]/20 border-2 border-[#1cb0f6] text-[#1cb0f6] flex items-center justify-center text-4xl mx-auto shadow-inner">
          📖
        </div>

        <div>
          <Badge variant="blue" className="mb-2">
            Lesson Session
          </Badge>
          <h1 className="text-2xl font-black text-white">{lesson.title}</h1>
          {lesson.description && (
            <p className="text-xs text-gray-400 mt-2">{lesson.description}</p>
          )}
        </div>

        {/* Lesson Overview Metrics */}
        <div className="grid grid-cols-3 gap-2 p-3 bg-[#131f24] rounded-2xl border border-[#37464f] text-center text-xs font-bold">
          <div>
            <span className="text-gray-400 block text-[10px] uppercase">Exercises</span>
            <span className="text-white text-sm font-black">{lesson.exercises.length}</span>
          </div>
          <div>
            <span className="text-gray-400 block text-[10px] uppercase">Reward</span>
            <span className="text-[#ffc800] text-sm font-black">⭐ +{lesson.xp_reward} XP</span>
          </div>
          <div>
            <span className="text-gray-400 block text-[10px] uppercase">Hearts</span>
            <span className="text-[#ff4b4b] text-sm font-black">❤️ {stats ? stats.hearts : 5}</span>
          </div>
        </div>

        <Button
          variant="primary"
          size="lg"
          className="w-full text-base py-4"
          loading={isStarting}
          onClick={onStart}
        >
          START LESSON →
        </Button>
      </Card>
    </div>
  );
};
