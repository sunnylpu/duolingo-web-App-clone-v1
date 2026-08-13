import React from "react";

interface EmptyStateProps {
  title?: string;
  message?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = "No items found",
  message = "There is no content available to display at this time.",
}) => {
  return (
    <div className="duo-card p-8 text-center space-y-2 my-4">
      <h4 className="font-bold text-gray-300 text-base">{title}</h4>
      <p className="text-xs text-gray-500 max-w-sm mx-auto">{message}</p>
    </div>
  );
};
