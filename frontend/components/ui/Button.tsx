import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "danger";
  size?: "sm" | "md" | "lg";
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  className = "",
  disabled,
  ...props
}) => {
  const variantStyles = {
    primary: "duo-button-green text-black font-bold",
    secondary: "bg-[#1cb0f6] text-white font-bold shadow-[0_4px_0_#1899d6] hover:bg-[#20b8ff] active:shadow-none active:translate-y-1",
    outline: "border-2 border-[#37464f] text-gray-200 font-bold hover:bg-[#37464f]/30",
    danger: "bg-[#ff4b4b] text-white font-bold shadow-[0_4px_0_#ea2b2b] hover:bg-[#ff5a5a] active:shadow-none active:translate-y-1",
  };

  const sizeStyles = {
    sm: "px-3 py-1.5 text-xs rounded-lg",
    md: "px-5 py-2.5 text-sm rounded-xl",
    lg: "px-6 py-3.5 text-base rounded-2xl",
  };

  return (
    <button
      className={`inline-flex items-center justify-center transition-all disabled:opacity-50 disabled:pointer-events-none ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};
