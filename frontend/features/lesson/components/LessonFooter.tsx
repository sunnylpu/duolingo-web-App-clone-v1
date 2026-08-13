import React from "react";
import { Button } from "@/components/ui/Button";

interface LessonFooterProps {
  onContinue: () => void;
  isLastExercise?: boolean;
}

export const LessonFooter: React.FC<LessonFooterProps> = ({
  onContinue,
  isLastExercise = false,
}) => {
  return (
    <footer className="fixed bottom-0 left-0 right-0 z-30 bg-[#182830] border-t border-[#37464f] p-4">
      <div className="max-w-2xl mx-auto flex justify-end">
        <Button
          variant="primary"
          size="lg"
          className="w-full sm:w-auto px-8 font-black tracking-wider"
          onClick={onContinue}
        >
          {isLastExercise ? "FINISH LESSON →" : "CONTINUE →"}
        </Button>
      </div>
    </footer>
  );
};
