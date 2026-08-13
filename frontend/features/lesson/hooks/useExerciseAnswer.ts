"use client";

import { useState } from "react";
import {
  lessonSessionService,
  AnswerSubmissionResult,
} from "../services/lesson-session-service";

export function useExerciseAnswer(lessonId: string, attemptId: string | number | null) {
  const [selectedAnswer, setSelectedAnswer] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [result, setResult] = useState<AnswerSubmissionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const submitAnswer = async (exerciseId: string) => {
    if (!attemptId || !selectedAnswer || isSubmitting) return;
    setIsSubmitting(true);
    setError(null);

    try {
      const res = await lessonSessionService.submitAnswer({
        lessonId,
        exerciseId,
        attemptId,
        answer: selectedAnswer,
      });
      setResult(res);
      return res;
    } catch (err: any) {
      setError(err?.message || "Failed to validate exercise answer.");
      return null;
    } finally {
      setIsSubmitting(false);
    }
  };

  const reset = () => {
    setSelectedAnswer("");
    setResult(null);
    setError(null);
    setIsSubmitting(false);
  };

  const feedbackState: "idle" | "correct" | "incorrect" = result
    ? result.is_correct
      ? "correct"
      : "incorrect"
    : "idle";

  return {
    selectedAnswer,
    setSelectedAnswer,
    isSubmitting,
    result,
    error,
    feedbackState,
    submitAnswer,
    reset,
  };
}
