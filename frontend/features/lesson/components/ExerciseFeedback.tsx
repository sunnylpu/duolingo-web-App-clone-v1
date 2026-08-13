import React from "react";
import { Button } from "@/components/ui/Button";

interface ExerciseFeedbackProps {
  status: "idle" | "correct" | "incorrect";
  correctAnswer?: string;
  isSubmitting?: boolean;
  canCheck?: boolean;
  onCheck?: () => void;
  onContinue?: () => void;
}

export const ExerciseFeedback: React.FC<ExerciseFeedbackProps> = ({
  status,
  correctAnswer,
  isSubmitting = false,
  canCheck = false,
  onCheck,
  onContinue,
}) => {
  if (status === "correct") {
    return (
      <footer
        className="fixed bottom-0 left-0 right-0 z-30 bg-[#58cc02]/10 border-t-2 border-[#58cc02] p-4 text-white animate-fadeIn"
        aria-live="polite"
      >
        <div className="max-w-2xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-[#58cc02] text-black font-black text-2xl flex items-center justify-center">
              ✓
            </div>
            <div>
              <h4 className="text-lg font-black text-[#58cc02]">Nice work!</h4>
              <p className="text-xs text-gray-300">You got it right.</p>
            </div>
          </div>
          <Button
            variant="success"
            size="lg"
            className="w-full sm:w-auto px-8"
            onClick={onContinue}
          >
            CONTINUE →
          </Button>
        </div>
      </footer>
    );
  }

  if (status === "incorrect") {
    return (
      <footer
        className="fixed bottom-0 left-0 right-0 z-30 bg-[#ff4b4b]/10 border-t-2 border-[#ff4b4b] p-4 text-white animate-fadeIn"
        aria-live="polite"
      >
        <div className="max-w-2xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-[#ff4b4b] text-white font-black text-2xl flex items-center justify-center">
              ✕
            </div>
            <div>
              <h4 className="text-lg font-black text-[#ff4b4b]">Not quite</h4>
              <p className="text-xs text-gray-300 font-bold">
                Correct answer: <span className="underline">{correctAnswer}</span>
              </p>
            </div>
          </div>
          <Button
            variant="danger"
            size="lg"
            className="w-full sm:w-auto px-8"
            onClick={onContinue}
          >
            CONTINUE →
          </Button>
        </div>
      </footer>
    );
  }

  return (
    <footer className="fixed bottom-0 left-0 right-0 z-30 bg-[#182830] border-t border-[#37464f] p-4">
      <div className="max-w-2xl mx-auto flex justify-end">
        <Button
          variant="primary"
          size="lg"
          className="w-full sm:w-auto px-8 font-black tracking-wider"
          disabled={!canCheck || isSubmitting}
          loading={isSubmitting}
          onClick={onCheck}
        >
          CHECK
        </Button>
      </div>
    </footer>
  );
};
