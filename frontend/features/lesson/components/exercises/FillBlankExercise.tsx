import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

interface FillBlankExerciseProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (answer: string) => void;
  onSubmit?: () => void;
  disabled?: boolean;
  feedbackStatus?: "idle" | "correct" | "incorrect";
}

export const FillBlankExercise: React.FC<FillBlankExerciseProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  onSubmit,
  disabled = false,
  feedbackStatus = "idle",
}) => {
  const sentenceBefore = exercise.data?.sentence_before || "Yo";
  const sentenceAfter = exercise.data?.sentence_after || "pan.";

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="blue">Fill in the Blank</Badge>
        <span className="text-xs text-gray-400 font-bold">Complete the missing word in the sentence</span>
      </div>

      <h2 className="text-xl sm:text-2xl font-black text-white">{exercise.prompt}</h2>

      <Card className="p-6 bg-[#182830] border-2 border-[#37464f] flex flex-wrap items-center justify-center gap-3 text-xl sm:text-2xl font-black text-white">
        <span>{sentenceBefore}</span>
        <input
          type="text"
          value={selectedAnswer}
          disabled={disabled}
          onChange={(e) => onSelectAnswer(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && selectedAnswer.trim() && onSubmit && !disabled) {
              e.preventDefault();
              onSubmit();
            }
          }}
          placeholder="___"
          className={`w-36 sm:w-44 p-2.5 text-center bg-[#131f24] border-b-4 rounded-xl text-xl sm:text-2xl font-black text-[#1cb0f6] focus:outline-none transition-colors disabled:opacity-60 ${
            feedbackStatus === "correct"
              ? "border-[#58cc02] text-[#58cc02]"
              : feedbackStatus === "incorrect"
              ? "border-[#ff4b4b] text-[#ff4b4b]"
              : "border-[#1cb0f6] focus:border-[#1cb0f6]"
          }`}
          autoFocus
        />
        <span>{sentenceAfter}</span>
      </Card>
      <p className="text-center text-[11px] text-gray-500 font-medium">Type the word and press Enter to submit</p>
    </div>
  );
};
