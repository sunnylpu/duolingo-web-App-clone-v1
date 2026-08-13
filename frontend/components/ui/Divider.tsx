import React from "react";

interface DividerProps {
  label?: string;
  className?: string;
}

export const Divider: React.FC<DividerProps> = ({ label, className = "" }) => {
  if (label) {
    return (
      <div className={`relative flex py-2 items-center ${className}`}>
        <div className="flex-grow border-t border-[#37464f]"></div>
        <span className="flex-shrink mx-4 text-xs font-bold text-gray-500 uppercase tracking-widest">
          {label}
        </span>
        <div className="flex-grow border-t border-[#37464f]"></div>
      </div>
    );
  }

  return <hr className={`border-t border-[#37464f] my-4 ${className}`} />;
};
