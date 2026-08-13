"use client";

import React, { useEffect, useState } from "react";
import { LessonDetail, UserStats } from "@/types";
import { LessonHeader } from "./LessonHeader";
import { LessonProgress } from "./LessonProgress";
import { ExerciseRenderer } from "./ExerciseRenderer";
import { ExerciseFeedback } from "./ExerciseFeedback";
import { ExitConfirmationModal } from "./ExitConfirmationModal";
import { OutOfHeartsModal } from "./OutOfHeartsModal";
import { LessonComplete } from "./LessonComplete";
import { LessonLoading } from "./LessonLoading";
import { ErrorState } from "@/components/feedback/ErrorState";
import { useLessonSession } from "../hooks/useLessonSession";
import { useExerciseAnswer } from "../hooks/useExerciseAnswer";
import { LessonIntro } from "./LessonIntro";

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
    completionResult,
    isExitModalOpen,
    isStarting,
    sessionError,
    startSession,
    completeSession,
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

  if (step === "completing") {
    return <LessonLoading />;
  }

  if (step === "completed") {
    return (
      <LessonComplete
        result={completionResult}
        onContinue={() => {
          window.location.href = "/learn";
        }}
      />
    );
  }

  if (step === "error") {
    return (
      <div className="max-w-md mx-auto py-12 px-4 space-y-4">
        <ErrorState
          title="Couldn't complete the lesson."
          message={sessionError || "Failed to communicate with backend."}
          onRetry={completeSession}
        />
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
