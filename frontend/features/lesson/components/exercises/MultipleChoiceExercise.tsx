import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { AudioButton } from "@/features/audio/components/AudioButton";

interface MultipleChoiceExerciseProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (answer: string) => void;
  disabled?: boolean;
  feedbackStatus?: "idle" | "correct" | "incorrect";
}

export const MultipleChoiceExercise: React.FC<MultipleChoiceExerciseProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  disabled = false,
  feedbackStatus = "idle",
}) => {
  const options: string[] =
    exercise.data?.options || ["Option A", "Option B", "Option C", "Option D"];

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Badge variant="blue">Multiple Choice</Badge>
          <span className="text-xs text-gray-400 font-bold">Select the correct option</span>
        </div>
        <AudioButton text={exercise.prompt} />
      </div>

      <h2 className="text-xl sm:text-2xl font-black text-white">{exercise.prompt}</h2>

      <div
        className="grid grid-cols-1 sm:grid-cols-2 gap-3"
        role="radiogroup"
        aria-label="Multiple choice options"
      >
        {options.map((opt: string, idx: number) => {
          const isSelected = selectedAnswer === opt;

          let cardStyle = "bg-[#182830] border-2 border-[#37464f] text-gray-200 hover:border-[#1cb0f6]";
          if (isSelected) {
            cardStyle = "bg-[#1cb0f6]/20 border-2 border-[#1cb0f6] text-white shadow-[0_4px_0_#1899d6]";
          }
          if (feedbackStatus === "correct" && isSelected) {
            cardStyle = "bg-[#58cc02]/20 border-2 border-[#58cc02] text-[#58cc02]";
          } else if (feedbackStatus === "incorrect" && isSelected) {
            cardStyle = "bg-[#ff4b4b]/20 border-2 border-[#ff4b4b] text-[#ff4b4b]";
          }

          return (
            <button
              key={idx}
              type="button"
              role="radio"
              aria-checked={isSelected}
              disabled={disabled}
              onClick={() => !disabled && onSelectAnswer(opt)}
              onKeyDown={(e) => {
                if ((e.key === " " || e.key === "Enter") && !disabled) {
                  e.preventDefault();
                  onSelectAnswer(opt);
                }
              }}
              className={`duo-card p-5 text-left text-base font-bold transition-all select-none cursor-pointer focus:outline-none focus-visible:ring-4 focus-visible:ring-[#1cb0f6] disabled:opacity-60 disabled:cursor-not-allowed ${cardStyle}`}
            >
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="w-7 h-7 rounded-xl border-2 border-current flex items-center justify-center text-xs font-black shrink-0">
                    {idx + 1}
                  </span>
                  <span>{opt}</span>
                </div>
                <AudioButton text={opt} size="sm" />
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
