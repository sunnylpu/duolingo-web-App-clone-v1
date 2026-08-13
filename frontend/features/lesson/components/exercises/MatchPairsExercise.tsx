import React, { useEffect, useState, useMemo } from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";

interface PairData {
  left: string;
  right: string;
}

interface MatchToken {
  id: string;
  text: string;
  side: "left" | "right";
  partnerText: string;
}

interface MatchPairsExerciseProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (answer: string) => void;
  disabled?: boolean;
  feedbackStatus?: "idle" | "correct" | "incorrect";
}

export const MatchPairsExercise: React.FC<MatchPairsExerciseProps> = ({
  exercise,
  onSelectAnswer,
  disabled = false,
  feedbackStatus = "idle",
}) => {
  const rawPairs: PairData[] = exercise.data?.pairs || [
    { left: "Hola", right: "Hello" },
    { left: "Gracias", right: "Thank you" },
    { left: "Adiós", right: "Goodbye" },
  ];

  // Derive left and right token arrays and shuffle them independently
  const leftTokens: MatchToken[] = useMemo(() => {
    const list = rawPairs.map((p, idx) => ({
      id: `left-${idx}-${p.left}`,
      text: p.left,
      side: "left" as const,
      partnerText: p.right,
    }));
    return [...list].sort(() => Math.random() - 0.5);
  }, [exercise.id]);

  const rightTokens: MatchToken[] = useMemo(() => {
    const list = rawPairs.map((p, idx) => ({
      id: `right-${idx}-${p.right}`,
      text: p.right,
      side: "right" as const,
      partnerText: p.left,
    }));
    return [...list].sort(() => Math.random() - 0.5);
  }, [exercise.id]);

  const [selectedLeft, setSelectedLeft] = useState<MatchToken | null>(null);
  const [selectedRight, setSelectedRight] = useState<MatchToken | null>(null);
  const [matchedIds, setMatchedIds] = useState<string[]>([]);
  const [confirmedPairs, setConfirmedPairs] = useState<[string, string][]>([]);
  const [wrongPairAlert, setWrongPairAlert] = useState<boolean>(false);

  // Evaluate pairing when both left and right tokens are selected
  useEffect(() => {
    if (selectedLeft && selectedRight) {
      // Check if pairing matches
      const isMatch =
        selectedLeft.partnerText.trim().toLowerCase() ===
        selectedRight.text.trim().toLowerCase();

      if (isMatch) {
        setMatchedIds((prev) => [...prev, selectedLeft.id, selectedRight.id]);
        setConfirmedPairs((prev) => [
          ...prev,
          [selectedLeft.text, selectedRight.text],
        ]);
        setSelectedLeft(null);
        setSelectedRight(null);
      } else {
        // Temporary wrong local pair visual feedback
        setWrongPairAlert(true);
        const timer = setTimeout(() => {
          setSelectedLeft(null);
          setSelectedRight(null);
          setWrongPairAlert(false);
        }, 800);
        return () => clearTimeout(timer);
      }
    }
  }, [selectedLeft, selectedRight]);

  // Update parent onSelectAnswer with structured answer when all pairs are matched
  useEffect(() => {
    if (confirmedPairs.length === rawPairs.length && rawPairs.length > 0) {
      // Pass JSON string or object representation of pairs
      onSelectAnswer(JSON.stringify({ pairs: confirmedPairs }));
    } else {
      onSelectAnswer("");
    }
  }, [confirmedPairs, rawPairs.length]);

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4 select-none">
      <div className="flex items-center gap-2">
        <Badge variant="yellow">Match Pairs</Badge>
        <span className="text-xs text-gray-400 font-bold">Tap matching pairs on left and right</span>
      </div>

      <h2 className="text-xl sm:text-2xl font-black text-white">{exercise.prompt}</h2>

      {wrongPairAlert && (
        <div className="p-3 bg-[#ff4b4b]/20 border border-[#ff4b4b] rounded-xl text-center text-xs font-black text-[#ff4b4b] animate-shake">
          ✕ Not a match! Try again.
        </div>
      )}

      <div className="grid grid-cols-2 gap-4">
        {/* Left Column */}
        <div className="space-y-3">
          <span className="text-[11px] text-gray-400 font-bold uppercase tracking-wider block text-center">
            Spanish
          </span>
          {leftTokens.map((token) => {
            const isMatched = matchedIds.includes(token.id);
            const isSelected = selectedLeft?.id === token.id;

            let cardStyle = "bg-[#182830] border-2 border-[#37464f] text-white hover:border-[#1cb0f6]";
            if (isMatched) {
              cardStyle = "bg-[#58cc02]/20 border-2 border-[#58cc02] text-[#58cc02] opacity-70 pointer-events-none";
            } else if (isSelected) {
              cardStyle = "bg-[#1cb0f6]/20 border-2 border-[#1cb0f6] text-[#1cb0f6] shadow-[0_4px_0_#1899d6]";
            } else if (wrongPairAlert && isSelected) {
              cardStyle = "bg-[#ff4b4b]/20 border-2 border-[#ff4b4b] text-[#ff4b4b]";
            }

            return (
              <button
                key={token.id}
                type="button"
                disabled={disabled || isMatched}
                onClick={() => !disabled && !isMatched && setSelectedLeft(token)}
                className={`duo-card w-full min-h-[52px] p-3 text-center text-sm font-black rounded-2xl transition-all cursor-pointer focus:outline-none disabled:cursor-not-allowed ${cardStyle}`}
                aria-label={`Match ${token.text}`}
              >
                <div className="flex items-center justify-center gap-2">
                  <span>{token.text}</span>
                  {isMatched && <span>✓</span>}
                </div>
              </button>
            );
          })}
        </div>

        {/* Right Column */}
        <div className="space-y-3">
          <span className="text-[11px] text-gray-400 font-bold uppercase tracking-wider block text-center">
            English
          </span>
          {rightTokens.map((token) => {
            const isMatched = matchedIds.includes(token.id);
            const isSelected = selectedRight?.id === token.id;

            let cardStyle = "bg-[#182830] border-2 border-[#37464f] text-white hover:border-[#1cb0f6]";
            if (isMatched) {
              cardStyle = "bg-[#58cc02]/20 border-2 border-[#58cc02] text-[#58cc02] opacity-70 pointer-events-none";
            } else if (isSelected) {
              cardStyle = "bg-[#1cb0f6]/20 border-2 border-[#1cb0f6] text-[#1cb0f6] shadow-[0_4px_0_#1899d6]";
            } else if (wrongPairAlert && isSelected) {
              cardStyle = "bg-[#ff4b4b]/20 border-2 border-[#ff4b4b] text-[#ff4b4b]";
            }

            return (
              <button
                key={token.id}
                type="button"
                disabled={disabled || isMatched}
                onClick={() => !disabled && !isMatched && setSelectedRight(token)}
                className={`duo-card w-full min-h-[52px] p-3 text-center text-sm font-black rounded-2xl transition-all cursor-pointer focus:outline-none disabled:cursor-not-allowed ${cardStyle}`}
                aria-label={`Match ${token.text}`}
              >
                <div className="flex items-center justify-center gap-2">
                  <span>{token.text}</span>
                  {isMatched && <span>✓</span>}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
