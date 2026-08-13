"use client";

import { useState, useEffect, useCallback } from "react";

interface UseTextToSpeechReturn {
  speak: (text: string, lang?: string) => void;
  stop: () => void;
  isSpeaking: boolean;
  isSupported: boolean;
}

export const useTextToSpeech = (): UseTextToSpeechReturn => {
  const [isSupported, setIsSupported] = useState<boolean>(false);
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);

  useEffect(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      setIsSupported(true);
    }
  }, []);

  const stop = useCallback(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, []);

  const speak = useCallback(
    (text: string, lang: string = "es-ES") => {
      if (!isSupported || !text) return;

      stop();

      try {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        utterance.rate = 0.9; // Slightly slower for language learners

        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = () => setIsSpeaking(false);

        window.speechSynthesis.speak(utterance);
      } catch (err) {
        console.warn("Speech synthesis failed:", err);
        setIsSpeaking(false);
      }
    },
    [isSupported, stop]
  );

  return { speak, stop, isSpeaking, isSupported };
};
