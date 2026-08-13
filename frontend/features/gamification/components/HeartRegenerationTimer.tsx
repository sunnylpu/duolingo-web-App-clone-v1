"use client";

import React, { useEffect, useState } from "react";

interface HeartRegenerationTimerProps {
  secondsUntilNext: number | null | undefined;
  onTimerComplete?: () => void;
}

export const HeartRegenerationTimer: React.FC<HeartRegenerationTimerProps> = ({
  secondsUntilNext,
  onTimerComplete,
}) => {
  const [remaining, setRemaining] = useState<number | null>(secondsUntilNext ?? null);

  useEffect(() => {
    setRemaining(secondsUntilNext ?? null);
  }, [secondsUntilNext]);

  useEffect(() => {
    if (remaining === null || remaining <= 0) return;

    const interval = setInterval(() => {
      setRemaining((prev) => {
        if (prev === null || prev <= 1) {
          clearInterval(interval);
          if (onTimerComplete) {
            onTimerComplete();
          }
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [remaining, onTimerComplete]);

  if (remaining === null || remaining <= 0) {
    return (
      <div className="text-xs font-bold text-[#58cc02] flex items-center justify-center gap-1">
        <span>❤️</span> Hearts Full!
      </div>
    );
  }

  const minutes = Math.floor(remaining / 60);
  const seconds = remaining % 60;
  const formatted = `${minutes.toString().padStart(2, "0")}:${seconds
    .toString()
    .padStart(2, "0")}`;

  return (
    <div className="text-xs font-bold text-gray-300 flex items-center justify-center gap-1.5 select-none">
      <span>⏱️ Next heart in</span>
      <span className="font-mono text-[#ff4b4b] bg-[#ff4b4b]/10 px-2 py-0.5 rounded-lg border border-[#ff4b4b]/30 font-black">
        {formatted}
      </span>
    </div>
  );
};
