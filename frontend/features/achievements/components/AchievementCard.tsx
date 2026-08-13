import React from "react";
import { UserAchievement } from "@/types";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";

interface AchievementCardProps {
  userAchievement: UserAchievement;
}

export const AchievementCard: React.FC<AchievementCardProps> = ({
  userAchievement,
}) => {
  const { achievement, is_earned, earned_at, progress = 0, target = 1 } = userAchievement;
  const percent = Math.min(100, Math.round((progress / Math.max(1, target)) * 100));

  return (
    <Card
      className={`p-4 transition-all border-2 select-none ${
        is_earned
          ? "bg-[#182830] border-[#ffc800] shadow-[0_4px_0_#cca000]"
          : "bg-[#131f24] border-[#37464f] opacity-80"
      }`}
    >
      <div className="flex items-start gap-4">
        {/* Icon Badge */}
        <div
          className={`w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shrink-0 font-bold border-2 ${
            is_earned
              ? "bg-[#ffc800]/20 border-[#ffc800] text-[#ffc800]"
              : "bg-[#37464f]/40 border-[#37464f] text-gray-500"
          }`}
        >
          {is_earned ? achievement.icon || "🏆" : "🔒"}
        </div>

        {/* Content */}
        <div className="flex-1 space-y-1.5">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-extrabold text-sm sm:text-base text-white">
              {achievement.name}
            </h3>
            {is_earned ? (
              <Badge variant="yellow">Unlocked</Badge>
            ) : (
              <Badge variant="gray">Locked</Badge>
            )}
          </div>

          <p className="text-xs text-gray-400 font-medium">
            {achievement.description}
          </p>

          {is_earned ? (
            earned_at && (
              <span className="text-[10px] text-gray-400 font-bold block pt-1">
                Earned on {new Date(earned_at).toLocaleDateString()}
              </span>
            )
          ) : (
            <div className="space-y-1 pt-1">
              <div className="flex justify-between text-[11px] font-bold text-gray-400">
                <span>Progress</span>
                <span>{progress} / {target}</span>
              </div>
              <ProgressBar value={percent} height="h-2" />
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
