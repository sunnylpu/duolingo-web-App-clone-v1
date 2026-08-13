"use client";

import { useState } from "react";
import { LessonDetail } from "@/types";
import { LessonAttempt, LessonSessionStep } from "../types/lesson-session";
import { lessonSessionService } from "../services/lesson-session-service";

export function useLessonSession(lesson: LessonDetail | null) {
  const [step, setStep] = useState<LessonSessionStep>("intro");
  const [attempt, setAttempt] = useState<LessonAttempt | null>(null);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState<number>(0);
  const [isExitModalOpen, setIsExitModalOpen] = useState<boolean>(false);
  const [isStarting, setIsStarting] = useState<boolean>(false);
  const [startError, setStartError] = useState<string | null>(null);

  const startSession = async () => {
    if (!lesson) return;
    setIsStarting(true);
    setStartError(null);

    try {
      const attemptRes = await lessonSessionService.startLessonSession(lesson.id);
      setAttempt(attemptRes);
      setStep("active_player");
      setCurrentExerciseIndex(0);
    } catch (err: any) {
      setStartError(err?.message || "Failed to start lesson session.");
    } finally {
      setIsStarting(false);
    }
  };

  const nextExercise = () => {
    if (!lesson) return;
    if (currentExerciseIndex < lesson.exercises.length - 1) {
      setCurrentExerciseIndex((prev) => prev + 1);
    } else {
      setStep("sequence_complete");
    }
  };

  const triggerOutOfHearts = () => {
    setStep("out_of_hearts");
  };

  const openExitModal = () => setIsExitModalOpen(true);
  const closeExitModal = () => setIsExitModalOpen(false);

  return {
    step,
    attempt,
    currentExerciseIndex,
    currentExercise: lesson?.exercises[currentExerciseIndex] || null,
    totalExercises: lesson?.exercises.length || 0,
    isExitModalOpen,
    isStarting,
    startError,
    startSession,
    nextExercise,
    triggerOutOfHearts,
    openExitModal,
    closeExitModal,
  };
}
