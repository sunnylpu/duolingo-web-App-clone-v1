"use client";

import React, { useEffect, useState } from "react";
import { achievementService, UserAchievement } from "@/services/achievement-service";
import { AchievementCategoryTabs } from "./AchievementCategoryTabs";
import { AchievementCard } from "./AchievementCard";
import { Card } from "@/components/ui/Card";

export const AchievementCenter: React.FC = () => {
  const [items, setItems] = useState<UserAchievement[]>([]);
  const [activeCategory, setActiveCategory] = useState<string>("ALL");
  const [loading, setLoading] = useState<boolean>(true);

  const loadAchievements = async (cat: string) => {
    setLoading(true);
    try {
      const data = await achievementService.getMyAchievements(cat);
      setItems(data);
    } catch (err) {
      console.error("Failed to load achievements:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAchievements(activeCategory);
  }, [activeCategory]);

  const earnedCount = items.filter((i) => i.is_earned).length;
  const totalCount = items.length;
  const legendaryEarned = items.filter((i) => i.is_earned && i.achievement.rarity === "legendary").length;
  const epicEarned = items.filter((i) => i.is_earned && i.achievement.rarity === "epic").length;

  return (
    <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-[#37464f] pb-4">
        <div>
          <h2 className="text-xl font-black text-white uppercase tracking-wider flex items-center gap-2">
            <span>🏆</span>
            <span>Achievement Center</span>
          </h2>
          <p className="text-xs text-gray-400 font-medium mt-0.5">
            Track your milestones, streaks, and course mastery badges
          </p>
        </div>

        {/* Stats Pill */}
        <div className="flex items-center gap-2 text-xs font-black bg-[#131f24] px-3 py-2 rounded-xl border border-[#37464f]">
          <span className="text-[#ffc800]">
            {earnedCount} / {totalCount} Unlocked
          </span>
          <span className="text-gray-500">•</span>
          <span className="text-[#a560ff]">{epicEarned} Epic</span>
          <span className="text-gray-500">•</span>
          <span className="text-[#ffc800]">{legendaryEarned} Legendary</span>
        </div>
      </div>

      {/* Category Tabs */}
      <AchievementCategoryTabs
        activeCategory={activeCategory}
        onSelectCategory={setActiveCategory}
      />

      {/* Achievement List */}
      {loading ? (
        <div className="py-8 text-center text-xs font-black text-gray-400 animate-pulse">
          Loading achievements...
        </div>
      ) : items.length === 0 ? (
        <div className="py-8 text-center text-xs font-medium text-gray-400">
          No achievements found for category "{activeCategory}".
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {items.map((item) => (
            <AchievementCard key={item.achievement.id} item={item} />
          ))}
        </div>
      )}
    </Card>
  );
};
