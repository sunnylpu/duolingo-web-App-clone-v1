import React from "react";
import { Exercise } from "@/types";
import { MultipleChoiceExercise } from "./exercises/MultipleChoiceExercise";
import { TranslateExercise } from "./exercises/TranslateExercise";
import { WordBankExercise } from "./exercises/WordBankExercise";
import { MatchPairsExercise } from "./exercises/MatchPairsExercise";
import { FillBlankExercise } from "./exercises/FillBlankExercise";
import { TypeAnswerExercise } from "./exercises/TypeAnswerExercise";

interface ExerciseRendererProps {
  exercise: Exercise | null;
}

export const ExerciseRenderer: React.FC<ExerciseRendererProps> = ({ exercise }) => {
  if (!exercise) {
    return (
      <div className="p-8 text-center text-gray-500 font-bold">
        No exercise content available.
      </div>
    );
  }

  switch (exercise.type) {
    case "multiple_choice":
      return <MultipleChoiceExercise exercise={exercise} />;
    case "translate":
      return <TranslateExercise exercise={exercise} />;
    case "word_bank":
      return <WordBankExercise exercise={exercise} />;
    case "match_pairs":
      return <MatchPairsExercise exercise={exercise} />;
    case "fill_blank":
      return <FillBlankExercise exercise={exercise} />;
    case "type_answer":
      return <TypeAnswerExercise exercise={exercise} />;
    default:
      return (
        <div className="p-8 text-center text-gray-400">
          <p className="font-bold text-white">{exercise.prompt}</p>
          <span className="text-xs text-gray-500 font-mono mt-2 block">
            Type: {exercise.type}
          </span>
        </div>
      );
  }
};
