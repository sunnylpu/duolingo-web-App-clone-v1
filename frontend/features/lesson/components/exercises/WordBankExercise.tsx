import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

interface ExerciseProps {
  exercise: Exercise;
}

export const WordBankExercise: React.FC<ExerciseProps> = ({ exercise }) => {
  const words = exercise.data?.words || ["Hola", "Buenos", "días", "gracias", "por", "favor"];

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="purple">Word Bank</Badge>
        <span className="text-xs text-gray-400 font-bold">Tap words to build translation</span>
      </div>

      <h2 className="text-xl font-black text-white">{exercise.prompt}</h2>

      <Card className="p-4 bg-[#131f24] min-h-[80px] border-dashed border-[#37464f]" />

      <div className="flex flex-wrap gap-2 justify-center">
        {words.map((w: string, idx: number) => (
          <span
            key={idx}
            className="px-4 py-2 bg-[#182830] border-2 border-[#37464f] rounded-xl text-sm font-bold text-white shadow-[0_3px_0_#37464f]"
          >
            {w}
          </span>
        ))}
      </div>
    </div>
  );
};
