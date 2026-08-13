import React from "react";

interface LessonProgressProps {
  currentIndex: number;
  totalExercises: number;
}

export const LessonProgress: React.FC<LessonProgressProps> = ({
  currentIndex,
  totalExercises,
}) => {
  return (
    <div className="text-center py-2">
      <span className="text-xs font-bold text-gray-400 uppercase tracking-widest">
        Exercise {currentIndex + 1} of {totalExercises}
      </span>
    </div>
  );
};
