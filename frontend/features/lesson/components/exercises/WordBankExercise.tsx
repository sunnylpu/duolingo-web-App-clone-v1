import React, { useEffect, useState } from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

interface WordToken {
  id: string;
  text: string;
}

interface WordBankExerciseProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (answer: string) => void;
  disabled?: boolean;
  feedbackStatus?: "idle" | "correct" | "incorrect";
}

export const WordBankExercise: React.FC<WordBankExerciseProps> = ({
  exercise,
  onSelectAnswer,
  disabled = false,
  feedbackStatus = "idle",
}) => {
  const initialWordTexts: string[] =
    exercise.data?.words || ["Hola", "Buenos", "días", "gracias", "por", "favor"];

  // Create unique tokens with IDs
  const [tokens] = useState<WordToken[]>(() =>
    initialWordTexts.map((w, idx) => ({ id: `word-${idx}-${w}`, text: w }))
  );

  const [availableIds, setAvailableIds] = useState<string[]>(() =>
    tokens.map((t) => t.id)
  );

  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  // Assembles string answer and updates parent selectedAnswer whenever selectedIds changes
  useEffect(() => {
    const assembled = selectedIds
      .map((id) => tokens.find((t) => t.id === id)?.text || "")
      .filter(Boolean)
      .join(" ");
    onSelectAnswer(assembled);
  }, [selectedIds, tokens]);

  const selectWord = (tokenId: string) => {
    if (disabled) return;
    setAvailableIds((prev) => prev.filter((id) => id !== tokenId));
    setSelectedIds((prev) => [...prev, tokenId]);
  };

  const removeWord = (tokenId: string) => {
    if (disabled) return;
    setSelectedIds((prev) => prev.filter((id) => id !== tokenId));
    setAvailableIds((prev) => [...prev, tokenId]);
  };

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4 select-none">
      <div className="flex items-center gap-2">
        <Badge variant="purple">Word Bank</Badge>
        <span className="text-xs text-gray-400 font-bold">Tap words to build translation</span>
      </div>

      <h2 className="text-xl sm:text-2xl font-black text-white">{exercise.prompt}</h2>

      {/* Answer Assembly Area */}
      <div className="space-y-2">
        <label className="text-xs text-gray-400 font-bold uppercase tracking-wider">Your Answer</label>
        <Card
          className={`p-4 min-h-[90px] border-2 rounded-2xl flex flex-wrap items-center gap-2 transition-colors ${
            feedbackStatus === "correct"
              ? "border-[#58cc02] bg-[#58cc02]/10"
              : feedbackStatus === "incorrect"
              ? "border-[#ff4b4b] bg-[#ff4b4b]/10"
              : "border-dashed border-[#37464f] bg-[#131f24]"
          }`}
        >
          {selectedIds.length === 0 ? (
            <span className="text-sm text-gray-500 font-bold italic">
              Tap words below to assemble your translation...
            </span>
          ) : (
            selectedIds.map((id) => {
              const token = tokens.find((t) => t.id === id);
              if (!token) return null;
              return (
                <button
                  key={token.id}
                  type="button"
                  disabled={disabled}
                  onClick={() => removeWord(token.id)}
                  className="px-4 py-2 bg-[#182830] border-2 border-[#1cb0f6] text-[#1cb0f6] rounded-xl text-base font-black shadow-[0_3px_0_#1899d6] hover:bg-[#1cb0f6]/20 focus:outline-none disabled:opacity-60 cursor-pointer animate-fadeIn"
                  aria-label={`Remove word ${token.text}`}
                >
                  {token.text}
                </button>
              );
            })
          )}
        </Card>
      </div>

      {/* Available Word Bank Pool */}
      <div className="space-y-2 pt-2">
        <label className="text-xs text-gray-400 font-bold uppercase tracking-wider">Word Pool</label>
        <div className="flex flex-wrap gap-2.5 justify-center min-h-[100px] p-4 bg-[#182830]/50 rounded-2xl border border-[#37464f]/40">
          {tokens.map((token) => {
            const isAvailable = availableIds.includes(token.id);

            return isAvailable ? (
              <button
                key={token.id}
                type="button"
                disabled={disabled}
                onClick={() => selectWord(token.id)}
                className="px-4 py-2.5 bg-[#182830] border-2 border-[#37464f] text-white rounded-xl text-base font-black shadow-[0_3px_0_#37464f] hover:border-[#1cb0f6] hover:text-[#1cb0f6] focus:outline-none disabled:opacity-60 cursor-pointer transition-all active:translate-y-0.5"
                aria-label={`Select word ${token.text}`}
              >
                {token.text}
              </button>
            ) : (
              <div
                key={token.id}
                className="px-4 py-2.5 bg-[#131f24] border-2 border-transparent text-transparent rounded-xl text-base font-black select-none pointer-events-none opacity-20"
              >
                {token.text}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
