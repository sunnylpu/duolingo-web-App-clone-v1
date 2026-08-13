import React from "react";
import { SkillPath } from "@/types";
import { ProgressRing } from "@/components/ui/ProgressRing";
import { CrownIndicator } from "./CrownIndicator";

interface SkillNodeProps {
  skill: SkillPath;
  onSelect: (skill: SkillPath) => void;
}

export const SkillNode: React.FC<SkillNodeProps> = ({ skill, onSelect }) => {
  const { status, title, completion_percent, crown_level } = skill;

  // Node base styles according to backend status
  const getNodeVisuals = () => {
    switch (status) {
      case "completed":
        return {
          bgColor: "bg-[#ffc800]",
          shadowColor: "shadow-[0_6px_0_#cca000]",
          ringColor: "text-[#ffc800]",
          icon: "⭐",
          label: `Completed skill: ${title}`,
        };
      case "in_progress":
        return {
          bgColor: "bg-[#1cb0f6]",
          shadowColor: "shadow-[0_6px_0_#1899d6]",
          ringColor: "text-[#1cb0f6]",
          icon: "📖",
          label: `In-progress skill: ${title}`,
        };
      case "available":
        return {
          bgColor: "bg-[#58cc02]",
          shadowColor: "shadow-[0_6px_0_#46a302]",
          ringColor: "text-[#58cc02]",
          icon: "▶",
          label: `Available skill: ${title}`,
        };
      case "locked":
      default:
        return {
          bgColor: "bg-[#37464f]",
          shadowColor: "shadow-[0_6px_0_#2b373e]",
          ringColor: "text-[#37464f]",
          icon: "🔒",
          label: `Locked skill: ${title}. Complete previous skill to unlock.`,
        };
    }
  };

  const visuals = getNodeVisuals();
  const isLocked = status === "locked";

  return (
    <div className="relative inline-flex flex-col items-center my-2 select-none">
      {/* Crown Level Indicator for completed/in-progress skills */}
      {crown_level > 0 && (
        <div className="absolute -top-3 z-10">
          <CrownIndicator level={crown_level} size="sm" />
        </div>
      )}

      {/* Main Interactive Button Wrapping Progress Ring */}
      <button
        onClick={() => onSelect(skill)}
        className={`relative group rounded-full focus:outline-none focus-visible:ring-4 focus-visible:ring-[#1cb0f6] cursor-pointer ${
          isLocked ? "opacity-75 cursor-not-allowed" : "hover:scale-105 transition-transform"
        }`}
        aria-label={visuals.label}
      >
        <ProgressRing
          percentage={completion_percent}
          size={84}
          strokeWidth={6}
          colorClass={visuals.ringColor}
        >
          {/* Inner Tactile Button Disc */}
          <div
            className={`w-16 h-16 rounded-full ${visuals.bgColor} ${visuals.shadowColor} flex items-center justify-center text-white text-xl font-black transition-all active:translate-y-1 active:shadow-none ${
              status === "available" ? "animate-pulse" : ""
            }`}
          >
            {visuals.icon}
          </div>
        </ProgressRing>
      </button>

      {/* Skill Title Below Node */}
      <div className="mt-2 text-center max-w-[120px]">
        <span className="text-skill-title text-gray-200 block truncate">
          {title}
        </span>
        {status === "in_progress" && (
          <span className="text-[10px] text-[#1cb0f6] font-bold block">
            {Math.round(completion_percent)}%
          </span>
        )}
      </div>
    </div>
  );
};
