import React from "react";
import { Exercise } from "@/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

interface ExerciseProps {
  exercise: Exercise;
}

export const MultipleChoiceExercise: React.FC<ExerciseProps> = ({ exercise }) => {
  const options = exercise.data?.options || ["Option A", "Option B", "Option C", "Option D"];

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="blue">Multiple Choice</Badge>
        <span className="text-xs text-gray-400 font-bold">Select the correct translation</span>
      </div>

      <h2 className="text-xl font-black text-white">{exercise.prompt}</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {options.map((opt: string, idx: number) => (
          <Card key={idx} hoverable className="p-4 text-center text-sm font-bold text-gray-200">
            {opt}
          </Card>
        ))}
      </div>
    </div>
  );
};
