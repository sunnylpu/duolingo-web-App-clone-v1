import React from "react";

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = "Something went wrong",
  message = "Failed to load backend data. Please ensure FastAPI server is running.",
  onRetry,
}) => {
  return (
    <div className="duo-card p-6 border-2 border-[#ff4b4b] bg-[#182830] text-center space-y-4 my-4 max-w-md mx-auto">
      <div className="w-12 h-12 rounded-full bg-[#ff4b4b]/20 text-[#ff4b4b] flex items-center justify-center mx-auto text-xl font-bold">
        !
      </div>
      <div>
        <h3 className="font-bold text-lg text-white">{title}</h3>
        <p className="text-sm text-gray-400 mt-1">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="duo-button-green px-4 py-2 text-black font-bold rounded-xl text-xs uppercase tracking-wider"
        >
          Retry Connection
        </button>
      )}
    </div>
  );
};
