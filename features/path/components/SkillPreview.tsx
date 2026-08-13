import React from "react";
import { SkillPath } from "@/types";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { CrownIndicator } from "./CrownIndicator";

interface SkillPreviewProps {
  skill: SkillPath | null;
  onClose: () => void;
  onStartLesson?: (skillId: string) => void;
}

export const SkillPreview: React.FC<SkillPreviewProps> = ({
  skill,
  onClose,
  onStartLesson,
}) => {
  if (!skill) return null;

  const isLocked = skill.status === "locked";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div
        className="duo-card w-full max-w-md p-6 bg-[#182830] border-2 border-[#37464f] space-y-5 relative shadow-2xl"
        role="dialog"
        aria-modal="true"
        aria-labelledby="skill-modal-title"
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-white font-black text-lg p-1"
          aria-label="Close skill preview"
        >
          ✕
        </button>

        {isLocked ? (
          /* Locked State Feedback */
          <div className="text-center space-y-4 py-2">
            <div className="w-16 h-16 rounded-full bg-[#37464f]/50 text-gray-400 flex items-center justify-center text-3xl mx-auto border-2 border-[#37464f]">
              🔒
            </div>
            <div>
              <h3 id="skill-modal-title" className="text-xl font-black text-white">
                Skill Locked
              </h3>
              <p className="text-xs text-gray-400 mt-1 max-w-xs mx-auto">
                Complete the previous skill on your path to unlock &quot;{skill.title}&quot;.
              </p>
            </div>
            <Button variant="outline" onClick={onClose} className="w-full">
              Got It
            </Button>
          </div>
        ) : (
          /* Unlocked (Available / In Progress / Completed) Preview */
          <div className="space-y-5">
            <div className="flex items-start justify-between gap-3">
              <div>
                <Badge variant={skill.status === "completed" ? "green" : "blue"}>
                  {skill.status.replace("_", " ")}
                </Badge>
                <h3 id="skill-modal-title" className="text-2xl font-black text-white mt-1">
                  {skill.title}
                </h3>
                {skill.description && (
                  <p className="text-xs text-gray-400 mt-1">{skill.description}</p>
                )}
              </div>
              <CrownIndicator level={skill.crown_level} size="lg" />
            </div>

            {/* Metrics */}
            <div className="grid grid-cols-2 gap-3 p-3 bg-[#131f24] rounded-xl border border-[#37464f] text-center text-xs">
              <div>
                <span className="text-gray-400 block font-bold">XP Reward</span>
                <span className="text-sm font-black text-[#ffc800]">⭐ {skill.xp_reward} XP</span>
              </div>
              <div>
                <span className="text-gray-400 block font-bold">Completion</span>
                <span className="text-sm font-black text-[#58cc02]">
                  {Math.round(skill.completion_percent)}%
                </span>
              </div>
            </div>

            <ProgressBar value={skill.completion_percent} height="h-3" />

            <div className="flex gap-3 pt-2">
              <Button
                variant="primary"
                size="lg"
                className="w-full"
                onClick={() => {
                  if (onStartLesson) {
                    onStartLesson(skill.id);
                  }
                  onClose();
                }}
              >
                START LESSON →
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
