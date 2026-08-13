import React from "react";
import { Exercise } from "@/types";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";

interface ExerciseProps {
  exercise: Exercise;
}

export const MatchPairsExercise: React.FC<ExerciseProps> = ({ exercise }) => {
  const pairs = exercise.data?.pairs || [
    { left: "Hola", right: "Hello" },
    { left: "Adiós", right: "Goodbye" },
  ];

  return (
    <div className="space-y-6 max-w-xl mx-auto py-4">
      <div className="flex items-center gap-2">
        <Badge variant="yellow">Match Pairs</Badge>
        <span className="text-xs text-gray-400 font-bold">Tap matching pairs</span>
      </div>

      <h2 className="text-xl font-black text-white">{exercise.prompt}</h2>

      <div className="grid grid-cols-2 gap-3">
        {pairs.map((p: any, idx: number) => (
          <React.Fragment key={idx}>
            <Card hoverable className="p-3 text-center text-sm font-bold text-gray-200">
              {p.left}
            </Card>
            <Card hoverable className="p-3 text-center text-sm font-bold text-gray-200">
              {p.right}
            </Card>
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};
