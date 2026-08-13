import React from "react";

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  icon: React.ReactNode;
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
}

export const IconButton: React.FC<IconButtonProps> = ({
  icon,
  variant = "ghost",
  size = "md",
  className = "",
  ...props
}) => {
  const sizeMap = {
    sm: "w-8 h-8 text-sm rounded-lg",
    md: "w-10 h-10 text-base rounded-xl",
    lg: "w-12 h-12 text-lg rounded-2xl",
  };

  const variantMap = {
    primary: "duo-button-green text-black",
    secondary: "duo-button-blue text-white",
    danger: "duo-button-red text-white",
    ghost: "text-gray-400 hover:text-white hover:bg-[#182830] active:bg-[#37464f]/30",
  };

  return (
    <button
      className={`inline-flex items-center justify-center transition-all cursor-pointer disabled:opacity-50 ${variantMap[variant]} ${sizeMap[size]} ${className}`}
      {...props}
    >
      {icon}
    </button>
  );
};
