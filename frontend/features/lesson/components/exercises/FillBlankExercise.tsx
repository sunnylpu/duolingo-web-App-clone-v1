import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";

interface ExerciseProps {
  exercise: Exercise;
}

export const FillBlankExercise: React.FC<ExerciseProps> = ({ exercise }) => {
  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="blue">Fill in the Blank</Badge>
        <span className="text-xs text-gray-400 font-bold">Complete the sentence</span>
      </div>

      <h2 className="text-xl font-black text-white">{exercise.prompt}</h2>

      <div className="p-4 bg-[#182830] border-2 border-[#37464f] rounded-xl text-lg font-bold flex items-center gap-2">
        <span>Yo</span>
        <span className="px-4 py-1 bg-[#131f24] border-b-4 border-[#1cb0f6] text-[#1cb0f6]">___</span>
        <span>español.</span>
      </div>
    </div>
  );
};
