"use client";

import React from "react";
import { useTextToSpeech } from "../hooks/useTextToSpeech";

interface AudioButtonProps {
  text: string;
  lang?: string;
  size?: "sm" | "md";
  className?: string;
}

export const AudioButton: React.FC<AudioButtonProps> = ({
  text,
  lang = "es-ES",
  size = "md",
  className = "",
}) => {
  const { speak, stop, isSpeaking, isSupported } = useTextToSpeech();

  if (!isSupported) {
    return null; // Gracefully degrade if Web Speech API is unsupported
  }

  const handleToggle = () => {
    if (isSpeaking) {
      stop();
    } else {
      speak(text, lang);
    }
  };

  const sizeClasses = {
    sm: "px-2.5 py-1 text-xs gap-1.5",
    md: "px-3.5 py-1.5 text-sm gap-2",
  };

  return (
    <button
      onClick={handleToggle}
      type="button"
      aria-label={`Play pronunciation for: ${text}`}
      title="Click to play audio pronunciation"
      className={`inline-flex items-center font-extrabold rounded-xl bg-[#1cb0f6]/10 text-[#1cb0f6] border border-[#1cb0f6]/40 hover:bg-[#1cb0f6]/20 transition-all select-none focus:outline-none focus:ring-2 focus:ring-[#1cb0f6] ${
        sizeClasses[size]
      } ${isSpeaking ? "animate-pulse border-[#1cb0f6]" : ""} ${className}`}
    >
      <span className="text-base">{isSpeaking ? "🔊" : "🔈"}</span>
      <span>{isSpeaking ? "Playing..." : "Listen"}</span>
    </button>
  );
};
