import React, { useEffect, useState } from "react";
import { SkillPath } from "@/types";
import { pathService, SkillPerformance } from "@/services/path-service";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { CrownIndicator } from "./CrownIndicator";

interface SkillPreviewProps {
  skill: SkillPath | null;
  onClose: () => void;
  onStartLesson?: (skillId: string) => void;
}

const MASTERY_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  mastered: { bg: "bg-[#ffc800]/20", text: "text-[#ffc800]", border: "border-[#ffc800]/30" },
  strong: { bg: "bg-[#58cc02]/20", text: "text-[#58cc02]", border: "border-[#58cc02]/30" },
  developing: { bg: "bg-[#1cb0f6]/20", text: "text-[#1cb0f6]", border: "border-[#1cb0f6]/30" },
  weak: { bg: "bg-[#ff4b4b]/20", text: "text-[#ff4b4b]", border: "border-[#ff4b4b]/30" },
};

export const SkillPreview: React.FC<SkillPreviewProps> = ({
  skill,
  onClose,
  onStartLesson,
}) => {
  const [perf, setPerf] = useState<SkillPerformance | null>(null);

  useEffect(() => {
    if (skill && skill.status !== "locked") {
      pathService
        .getSkillPerformance(skill.id)
        .then(setPerf)
        .catch(() => setPerf(null));
    }
  }, [skill]);

  if (!skill) return null;

  const isLocked = skill.status === "locked";
  const mState = perf?.mastery_state || "weak";
  const mTheme = MASTERY_COLORS[mState] || MASTERY_COLORS.weak;

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
                {skill.prerequisite_title
                  ? `Complete "${skill.prerequisite_title}" to unlock "${skill.title}".`
                  : `Complete the previous prerequisite skill to unlock "${skill.title}".`}
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
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant={skill.status === "completed" ? "green" : "blue"}>
                    {skill.status.replace("_", " ")}
                  </Badge>
                  {perf && (
                    <span
                      className={`px-2 py-0.5 text-[10px] uppercase font-black tracking-wider rounded-full border ${mTheme.bg} ${mTheme.text} ${mTheme.border}`}
                    >
                      {perf.mastery_state}
                    </span>
                  )}
                </div>
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
            <div className="grid grid-cols-3 gap-2 p-3 bg-[#131f24] rounded-xl border border-[#37464f] text-center text-xs">
              <div>
                <span className="text-gray-400 block font-bold">Progress</span>
                <span className="text-sm font-black text-[#58cc02]">
                  {Math.round(skill.completion_percent)}%
                </span>
              </div>
              <div>
                <span className="text-gray-400 block font-bold">Accuracy</span>
                <span className="text-sm font-black text-[#1cb0f6]">
                  {perf ? `${Math.round(perf.accuracy_percent)}%` : "100%"}
                </span>
              </div>
              <div>
                <span className="text-gray-400 block font-bold">Mastery</span>
                <span className="text-sm font-black text-[#ffc800]">
                  {perf ? perf.mastery_score : Math.round(skill.completion_percent * 0.5)}
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
