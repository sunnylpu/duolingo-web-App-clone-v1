import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";

interface ExerciseProps {
  exercise: Exercise;
}

export const TypeAnswerExercise: React.FC<ExerciseProps> = ({ exercise }) => {
  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="green">Type Answer</Badge>
        <span className="text-xs text-gray-400 font-bold">Write your response in target language</span>
      </div>

      <h2 className="text-xl font-black text-white">{exercise.prompt}</h2>

      <textarea
        rows={3}
        className="w-full p-4 bg-[#182830] border-2 border-[#37464f] rounded-2xl text-white font-bold text-base focus:border-[#1cb0f6] focus:outline-none resize-none placeholder-gray-500"
        placeholder="Type in Spanish..."
        readOnly
      />
    </div>
  );
};
