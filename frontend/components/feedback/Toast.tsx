import React from "react";

interface ToastProps {
  message: string;
  type?: "info" | "success" | "error";
  onClose?: () => void;
}

export const Toast: React.FC<ToastProps> = ({
  message,
  type = "info",
  onClose,
}) => {
  const colorMap = {
    info: "border-[#1cb0f6] bg-[#1cb0f6]/10 text-[#1cb0f6]",
    success: "border-[#58cc02] bg-[#58cc02]/10 text-[#58cc02]",
    error: "border-[#ff4b4b] bg-[#ff4b4b]/10 text-[#ff4b4b]",
  };

  return (
    <div
      className={`fixed bottom-16 right-4 md:bottom-6 md:right-6 border-2 px-4 py-3 rounded-xl flex items-center gap-3 shadow-lg z-50 text-sm font-medium ${colorMap[type]}`}
    >
      <span>{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          className="text-xs opacity-70 hover:opacity-100 font-bold ml-2"
        >
          ✕
        </button>
      )}
    </div>
  );
};
