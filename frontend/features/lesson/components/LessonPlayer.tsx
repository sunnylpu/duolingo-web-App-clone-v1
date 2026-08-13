"use client";

import React, { useEffect, useState } from "react";
import { LessonDetail, UserStats } from "@/types";
import { LessonHeader } from "./LessonHeader";
import { LessonProgress } from "./LessonProgress";
import { ExerciseRenderer } from "./ExerciseRenderer";
import { ExerciseFeedback } from "./ExerciseFeedback";
import { ExitConfirmationModal } from "./ExitConfirmationModal";
import { OutOfHeartsModal } from "./OutOfHeartsModal";
import { useLessonSession } from "../hooks/useLessonSession";
import { useExerciseAnswer } from "../hooks/useExerciseAnswer";
import { LessonIntro } from "./LessonIntro";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

interface LessonPlayerProps {
  lesson: LessonDetail;
  stats?: UserStats | null;
}

export const LessonPlayer: React.FC<LessonPlayerProps> = ({
  lesson,
  stats,
}) => {
  const {
    step,
    attempt,
    currentExerciseIndex,
    currentExercise,
    totalExercises,
    isExitModalOpen,
    isStarting,
    startSession,
    nextExercise,
    triggerOutOfHearts,
    openExitModal,
    closeExitModal,
  } = useLessonSession(lesson);

  const [heartsRemaining, setHeartsRemaining] = useState<number>(stats?.hearts ?? 5);

  const attemptId = attempt?.attempt_id || null;

  const {
    selectedAnswer,
    setSelectedAnswer,
    isSubmitting,
    result,
    feedbackState,
    submitAnswer,
    reset: resetAnswer,
  } = useExerciseAnswer(lesson.id, attemptId);

  // Reset exercise selection whenever current exercise index changes
  useEffect(() => {
    resetAnswer();
  }, [currentExerciseIndex]);

  // Update hearts state when backend returns updated hearts_remaining
  useEffect(() => {
    if (result && typeof result.hearts_remaining === "number") {
      setHeartsRemaining(result.hearts_remaining);
    }
  }, [result]);

  const handleCheck = async () => {
    if (!currentExercise) return;
    const res = await submitAnswer(currentExercise.id);
    if (res && res.hearts_remaining === 0 && !res.is_correct) {
      // User ran out of hearts on this answer
      triggerOutOfHearts();
    }
  };

  const handleContinue = () => {
    if (heartsRemaining <= 0) {
      triggerOutOfHearts();
      return;
    }
    resetAnswer();
    nextExercise();
  };

  if (step === "intro") {
    return (
      <LessonIntro
        lesson={lesson}
        stats={stats}
        isStarting={isStarting}
        onStart={startSession}
      />
    );
  }

  if (step === "sequence_complete") {
    return (
      <div className="max-w-md mx-auto py-12 px-4 text-center">
        <Card className="p-8 space-y-6 bg-[#182830] border-2 border-[#58cc02] shadow-2xl">
          <div className="w-20 h-20 rounded-full bg-[#58cc02]/20 border-2 border-[#58cc02] text-[#58cc02] flex items-center justify-center text-4xl mx-auto">
            🎉
          </div>
          <div>
            <h2 className="text-2xl font-black text-white">Sequence Completed!</h2>
            <p className="text-xs text-gray-400 mt-2">
              You reviewed all {totalExercises} exercises in this session.
            </p>
          </div>
          <Button
            variant="primary"
            size="lg"
            className="w-full"
            onClick={() => {
              window.location.href = "/learn";
            }}
          >
            RETURN TO PATH →
          </Button>
        </Card>
      </div>
    );
  }

  const isAnswered = feedbackState !== "idle";

  return (
    <div className="min-h-screen bg-[#131f24] flex flex-col justify-between pb-28">
      {/* Header with real-time hearts */}
      <LessonHeader
        currentIndex={currentExerciseIndex}
        totalExercises={totalExercises}
        stats={stats}
        heartsOverride={heartsRemaining}
        onExit={openExitModal}
      />

      {/* Main Exercise Area */}
      <main className="flex-1 max-w-2xl w-full mx-auto p-4 flex flex-col justify-center">
        <LessonProgress
          currentIndex={currentExerciseIndex}
          totalExercises={totalExercises}
        />
        <ExerciseRenderer
          exercise={currentExercise}
          selectedAnswer={selectedAnswer}
          onSelectAnswer={setSelectedAnswer}
          onSubmit={handleCheck}
          disabled={isSubmitting || isAnswered || heartsRemaining <= 0}
          feedbackStatus={feedbackState}
        />
      </main>

      {/* Interactive Bottom Feedback & CTA Bar */}
      <ExerciseFeedback
        status={feedbackState}
        correctAnswer={result?.correct_answer}
        heartsLost={result?.hearts_lost ?? 0}
        heartsRemaining={heartsRemaining}
        isSubmitting={isSubmitting}
        canCheck={Boolean(selectedAnswer.trim()) && heartsRemaining > 0}
        onCheck={handleCheck}
        onContinue={handleContinue}
      />

      {/* Exit Confirmation Dialog */}
      <ExitConfirmationModal
        isOpen={isExitModalOpen}
        onStay={closeExitModal}
        onLeave={() => {
          window.location.href = "/learn";
        }}
      />

      {/* Out of Hearts Modal */}
      <OutOfHeartsModal
        isOpen={step === "out_of_hearts"}
        onExit={() => {
          window.location.href = "/learn";
        }}
      />
    </div>
  );
};
