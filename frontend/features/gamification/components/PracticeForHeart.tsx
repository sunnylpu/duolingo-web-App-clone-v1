"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";

interface PracticeForHeartProps {
  onClose: () => void;
  onSuccess: () => void;
}

export const PracticeForHeart: React.FC<PracticeForHeartProps> = ({
  onClose,
  onSuccess,
}) => {
  const [selectedOption, setSelectedOption] = useState<string>("");
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<{ isCorrect: boolean; message: string } | null>(null);

  const handleSubmit = async () => {
    if (!selectedOption) return;
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/gamification/practice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          exercise_id: "ex_practice_default",
          answer: selectedOption,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data?.error?.message || "Practice submission failed.");
      }

      if (data.is_correct) {
        setFeedback({
          isCorrect: true,
          message: "EXCELLENT! You recovered 1 heart! ❤️",
        });
        setTimeout(() => {
          onSuccess();
        }, 1500);
      } else {
        setFeedback({
          isCorrect: false,
          message: `INCORRECT. Correct answer is "${data.correct_answer}".`,
        });
      }
    } catch (err: any) {
      setError(err?.message || "Could not process practice answer.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn select-none">
      <div className="duo-card w-full max-w-md p-6 bg-[#182830] border-2 border-[#1cb0f6] space-y-6 relative shadow-2xl">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white font-black text-lg p-1"
        >
          ✕
        </button>

        <div className="text-center space-y-2">
          <div className="w-14 h-14 rounded-full bg-[#1cb0f6]/20 border-2 border-[#1cb0f6] text-[#1cb0f6] flex items-center justify-center text-3xl mx-auto font-black">
            🏋️
          </div>
          <h2 className="text-2xl font-black text-white">Practice for a Heart</h2>
          <p className="text-xs text-gray-400">Answer correctly to recover +1 ❤️</p>
        </div>

        {/* Exercise Prompt */}
        <div className="p-4 bg-[#131f24] rounded-2xl border border-[#37464f] space-y-4">
          <div className="text-sm font-extrabold text-white text-center">
            Translate to Spanish: <span className="text-[#1cb0f6]">&quot;Hello&quot;</span>
          </div>

          <div className="grid grid-cols-2 gap-2">
            {["Hola", "Adiós", "Gracias", "Por favor"].map((option) => (
              <button
                key={option}
                onClick={() => setSelectedOption(option)}
                className={`p-3 rounded-xl font-black text-sm transition-all border-2 ${
                  selectedOption === option
                    ? "bg-[#1cb0f6] text-white border-[#1899d6] shadow-[0_3px_0_#1899d6]"
                    : "bg-[#182830] text-gray-200 border-[#37464f] hover:border-gray-400"
                }`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="p-3 bg-[#ff4b4b]/20 border border-[#ff4b4b] rounded-xl text-xs font-bold text-[#ff4b4b] text-center">
            {error}
          </div>
        )}

        {feedback && (
          <div
            className={`p-3 rounded-xl text-xs font-black text-center ${
              feedback.isCorrect
                ? "bg-[#58cc02]/20 border border-[#58cc02] text-[#58cc02]"
                : "bg-[#ff4b4b]/20 border border-[#ff4b4b] text-[#ff4b4b]"
            }`}
          >
            {feedback.message}
          </div>
        )}

        <div className="flex gap-3">
          <Button variant="outline" onClick={onClose} className="w-1/2">
            Cancel
          </Button>
          <Button
            variant="primary"
            disabled={!selectedOption || submitting || Boolean(feedback?.isCorrect)}
            onClick={handleSubmit}
            className="w-1/2"
          >
            {submitting ? "Checking..." : "CHECK →"}
          </Button>
        </div>
      </div>
    </div>
  );
};
