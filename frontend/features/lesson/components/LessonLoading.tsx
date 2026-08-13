import React from "react";
import { LoadingState } from "@/components/feedback/LoadingState";

export const LessonLoading: React.FC = () => {
  return (
    <div className="min-h-[70vh] flex items-center justify-center p-4">
      <LoadingState message="Preparing lesson session..." />
    </div>
  );
};
