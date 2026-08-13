"use client";

import React, { useState } from "react";
import { Button } from "@/components/ui/Button";
import { HeartRegenerationTimer } from "./HeartRegenerationTimer";
import { PracticeForHeart } from "./PracticeForHeart";

interface OutOfHeartsModalProps {
  hearts: number;
  maxHearts?: number;
  secondsUntilNext?: number | null;
  onClose: () => void;
  onRefreshStats: () => void;
}

export const OutOfHeartsModal: React.FC<OutOfHeartsModalProps> = ({
  hearts,
  maxHearts = 5,
  secondsUntilNext,
  onClose,
  onRefreshStats,
}) => {
  const [showPractice, setShowPractice] = useState<boolean>(false);
  const [refilling, setRefilling] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleMockRefill = async () => {
    setRefilling(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/gamification/hearts/refill", {
        method: "POST",
      });
      if (!res.ok) {
        throw new Error("Heart refill failed.");
      }
      onRefreshStats();
      onClose();
    } catch (err: any) {
      setError(err?.message || "Could not refill hearts.");
    } finally {
      setRefilling(false);
    }
  };

  if (showPractice) {
    return (
      <PracticeForHeart
        onClose={() => setShowPractice(false)}
        onSuccess={() => {
          setShowPractice(false);
          onRefreshStats();
          onClose();
        }}
      />
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn select-none">
      <div className="duo-card w-full max-w-md p-6 bg-[#182830] border-2 border-[#ff4b4b] space-y-6 relative shadow-2xl text-center">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white font-black text-lg p-1"
        >
          ✕
        </button>

        {/* Header Icon */}
        <div className="w-20 h-20 rounded-full bg-[#ff4b4b]/20 border-4 border-[#ff4b4b] text-[#ff4b4b] flex items-center justify-center text-4xl mx-auto motion-safe:animate-bounce">
          ❤️
        </div>

        <div>
          <h2 className="text-2xl font-black text-white">Out of Hearts!</h2>
          <p className="text-xs text-gray-400 font-medium mt-1">
            You need hearts to continue starting lessons and exercises.
          </p>
        </div>

        {/* Countdown Timer */}
        <div className="p-3 bg-[#131f24] rounded-2xl border border-[#37464f]">
          <HeartRegenerationTimer
            secondsUntilNext={secondsUntilNext}
            onTimerComplete={onRefreshStats}
          />
        </div>

        {error && (
          <div className="p-3 bg-[#ff4b4b]/20 border border-[#ff4b4b] rounded-xl text-xs font-bold text-[#ff4b4b]">
            {error}
          </div>
        )}

        {/* Recovery Options */}
        <div className="space-y-3">
          <Button
            variant="primary"
            size="lg"
            className="w-full bg-[#1cb0f6] border-[#1899d6] hover:bg-[#1cb0f6]/90 shadow-[0_4px_0_#1899d6]"
            onClick={() => setShowPractice(true)}
          >
            🏋️ PRACTICE FOR HEART (+1 ❤️)
          </Button>

          <Button
            variant="secondary"
            size="lg"
            disabled={refilling}
            className="w-full"
            onClick={handleMockRefill}
          >
            {refilling ? "Refilling..." : "⚡ MOCK REFILL (5/5 ❤️)"}
          </Button>
        </div>

        <Button variant="outline" onClick={onClose} className="w-full">
          EXIT
        </Button>
      </div>
    </div>
  );
};
