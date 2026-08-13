import React from "react";

interface PathConnectorProps {
  offset?: "center" | "left" | "right";
}

export const PathConnector: React.FC<PathConnectorProps> = ({
  offset = "center",
}) => {
  return (
    <div className="flex justify-center my-1 select-none pointer-events-none">
      <svg width="40" height="32" viewBox="0 0 40 32" fill="none">
        <path
          d={
            offset === "left"
              ? "M20 0 C20 16 10 16 10 32"
              : offset === "right"
              ? "M20 0 C20 16 30 16 30 32"
              : "M20 0 L20 32"
          }
          stroke="#37464f"
          strokeWidth="4"
          strokeDasharray="6 4"
          strokeLinecap="round"
        />
      </svg>
    </div>
  );
};
