"use client";

import React, { useEffect, useState } from "react";

export type ToastVariant = "success" | "info" | "warning" | "error";

export interface ToastProps {
  id?: string;
  message: string;
  variant?: ToastVariant;
  duration?: number;
  onClose?: () => void;
}

export const Toast: React.FC<ToastProps> = ({
  message,
  variant = "success",
  duration = 3000,
  onClose,
}) => {
  const [visible, setVisible] = useState<boolean>(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      if (onClose) onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  if (!visible) return null;

  const variantStyles = {
    success: "bg-[#58cc02] text-black border-[#46a302]",
    info: "bg-[#1cb0f6] text-white border-[#1899d6]",
    warning: "bg-[#ffc800] text-black border-[#e5b200]",
    error: "bg-[#ff4b4b] text-white border-[#ea2b2b]",
  };

  const icons = {
    success: "🎉",
    info: "💡",
    warning: "⚡",
    error: "⚠️",
  };

  return (
    <div
      role="status"
      aria-live="polite"
      className={`fixed bottom-6 right-6 z-50 flex items-center gap-3 px-4 py-3 rounded-2xl border-2 font-black text-sm shadow-2xl transition-all duration-300 animate-slideUp ${variantStyles[variant]}`}
    >
      <span className="text-xl">{icons[variant]}</span>
      <span>{message}</span>
      <button
        onClick={() => {
          setVisible(false);
          if (onClose) onClose();
        }}
        className="ml-2 font-bold opacity-70 hover:opacity-100 p-1"
        aria-label="Dismiss toast"
      >
        ✕
      </button>
    </div>
  );
};
