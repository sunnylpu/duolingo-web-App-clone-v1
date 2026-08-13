import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

interface ExerciseProps {
  exercise: Exercise;
}

export const TranslateExercise: React.FC<ExerciseProps> = ({ exercise }) => {
  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="green">Translate</Badge>
        <span className="text-xs text-gray-400 font-bold">Translate this sentence</span>
      </div>

      <h2 className="text-xl font-black text-white">{exercise.prompt}</h2>

      <Card className="p-4 bg-[#131f24] min-h-[100px] border-dashed text-sm text-gray-400">
        Type or assemble your translation here...
      </Card>
    </div>
  );
};
