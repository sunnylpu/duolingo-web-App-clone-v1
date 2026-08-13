import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

interface TranslateExerciseProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (answer: string) => void;
  onSubmit?: () => void;
  disabled?: boolean;
  feedbackStatus?: "idle" | "correct" | "incorrect";
}

export const TranslateExercise: React.FC<TranslateExerciseProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  onSubmit,
  disabled = false,
  feedbackStatus = "idle",
}) => {
  const sourceText = exercise.data?.source_text || exercise.prompt;

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="green">Translate</Badge>
        <span className="text-xs text-gray-400 font-bold">Translate this sentence</span>
      </div>

      <Card className="p-6 bg-[#182830] border-2 border-[#37464f] flex items-center gap-4">
        <div className="w-12 h-12 rounded-full bg-[#1cb0f6]/20 border-2 border-[#1cb0f6] text-[#1cb0f6] flex items-center justify-center text-xl shrink-0 font-bold">
          🗣️
        </div>
        <div>
          <h2 className="text-xl sm:text-2xl font-black text-white">{sourceText}</h2>
          <p className="text-xs text-gray-400 mt-1 font-medium">Write the translation in target language</p>
        </div>
      </Card>

      <div className="space-y-2">
        <label htmlFor="translate-input" className="sr-only">
          Translate answer
        </label>
        <textarea
          id="translate-input"
          rows={3}
          value={selectedAnswer}
          disabled={disabled}
          onChange={(e) => onSelectAnswer(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey && selectedAnswer.trim() && onSubmit && !disabled) {
              e.preventDefault();
              onSubmit();
            }
          }}
          placeholder="Type translation here..."
          className={`w-full p-4 bg-[#182830] border-2 rounded-2xl text-white font-bold text-lg focus:outline-none transition-colors resize-none disabled:opacity-60 ${
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
