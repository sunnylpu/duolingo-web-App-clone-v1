import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";

interface TypeAnswerExerciseProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (answer: string) => void;
  onSubmit?: () => void;
  disabled?: boolean;
  feedbackStatus?: "idle" | "correct" | "incorrect";
}

export const TypeAnswerExercise: React.FC<TypeAnswerExerciseProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  onSubmit,
  disabled = false,
  feedbackStatus = "idle",
}) => {
  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="green">Type Answer</Badge>
        <span className="text-xs text-gray-400 font-bold">Write your response in target language</span>
      </div>

      <h2 className="text-xl sm:text-2xl font-black text-white">{exercise.prompt}</h2>

      <div className="space-y-2">
        <label htmlFor="type-answer-input" className="sr-only">
          Type your translation
        </label>
        <input
          id="type-answer-input"
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
          placeholder="Type in Spanish..."
          className={`w-full p-4 bg-[#182830] border-2 rounded-2xl text-white font-bold text-lg focus:outline-none transition-colors disabled:opacity-60 ${
            feedbackStatus === "correct"
              ? "border-[#58cc02] bg-[#58cc02]/10"
              : feedbackStatus === "incorrect"
              ? "border-[#ff4b4b] bg-[#ff4b4b]/10"
              : "border-[#37464f] focus:border-[#1cb0f6]"
          }`}
          autoFocus
        />
        <p className="text-[11px] text-gray-500 font-medium">Press Enter to submit</p>
      </div>
    </div>
  );
};
