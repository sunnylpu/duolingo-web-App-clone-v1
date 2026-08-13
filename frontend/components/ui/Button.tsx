import React from "react";

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "success" | "danger" | "ghost" | "outline";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  className = "",
  disabled,
  ...props
}) => {
  const variantStyles = {
    primary: "duo-button-green text-black font-extrabold",
    secondary: "duo-button-blue text-white font-extrabold",
    success: "duo-button-green text-black font-extrabold",
    danger: "duo-button-red text-white font-extrabold",
    outline: "border-2 border-[#37464f] text-gray-200 font-extrabold hover:bg-[#37464f]/30 active:bg-[#37464f]/50",
    ghost: "text-gray-400 font-bold hover:text-white hover:bg-[#182830]",
  };

  const sizeStyles = {
    sm: "px-3 py-1.5 text-xs rounded-xl",
    md: "px-5 py-2.5 text-sm rounded-2xl",
    lg: "px-6 py-3.5 text-base rounded-2xl",
  };

  const isBtnDisabled = disabled || loading;

  return (
    <button
      className={`inline-flex items-center justify-center gap-2 transition-all cursor-pointer select-none disabled:opacity-50 disabled:pointer-events-none ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={isBtnDisabled}
      {...props}
    >
      {loading ? (
        <>
          <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
          <span>Loading...</span>
        </>
      ) : (
        children
      )}
    </button>
  );
};
