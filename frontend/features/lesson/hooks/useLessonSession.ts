"use client";

import { useState } from "react";
import { LessonDetail } from "@/types";
import { LessonAttempt, LessonSessionStep } from "../types/lesson-session";
import {
  lessonSessionService,
  LessonCompleteResult,
} from "../services/lesson-session-service";

export function useLessonSession(lesson: LessonDetail | null) {
  const [step, setStep] = useState<LessonSessionStep>("intro");
  const [attempt, setAttempt] = useState<LessonAttempt | null>(null);
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState<number>(0);
  const [completionResult, setCompletionResult] = useState<LessonCompleteResult | null>(null);
  const [isExitModalOpen, setIsExitModalOpen] = useState<boolean>(false);
  const [isStarting, setIsStarting] = useState<boolean>(false);
  const [sessionError, setSessionError] = useState<string | null>(null);

  const startSession = async () => {
    if (!lesson) return;
    setIsStarting(true);
    setSessionError(null);

    try {
      const attemptRes = await lessonSessionService.startLessonSession(lesson.id);
      setAttempt(attemptRes);
      setStep("active_player");
      setCurrentExerciseIndex(0);
    } catch (err: any) {
      setSessionError(err?.message || "Failed to start lesson session.");
    } finally {
      setIsStarting(false);
    }
  };

  const completeSession = async () => {
    if (!lesson || !attempt) return;
    setStep("completing");
    setSessionError(null);

    try {
      const res = await lessonSessionService.completeLessonSession({
        lessonId: lesson.id,
        attemptId: attempt.attempt_id,
      });
      setCompletionResult(res);
      setStep("completed");
    } catch (err: any) {
      setSessionError(err?.message || "Failed to complete lesson.");
      setStep("error");
    }
  };

  const nextExercise = () => {
    if (!lesson) return;
    if (currentExerciseIndex < lesson.exercises.length - 1) {
      setCurrentExerciseIndex((prev) => prev + 1);
    } else {
      completeSession();
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
  };
}
