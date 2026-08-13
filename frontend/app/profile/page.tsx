"use client";

import { useEffect, useState } from "react";
import { userService } from "@/services/user-service";
import { achievementService } from "@/services/achievement-service";
import { User, UserStats, UserAchievement } from "@/types";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [achievements, setAchievements] = useState<UserAchievement[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    setLoading(true);
    setError(null);
    try {
      const [userRes, statsRes, achRes] = await Promise.all([
        userService.getCurrentUser(),
        userService.getUserStats(),
        achievementService.getMyAchievements(),
      ]);
      setUser(userRes);
      setStats(statsRes);
      setAchievements(achRes);
    } catch (err: any) {
      setError(err?.message || "Failed to load user profile from backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, []);

  if (loading) {
    return <LoadingState message="Loading profile data..." fullPage />;
  }

  if (error || !user || !stats) {
    return (
      <ErrorState
        title="Profile Unavailable"
        message={error || "Could not retrieve user profile."}
        onRetry={loadProfile}
      />
    );
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Profile Header Card */}
      <Card className="p-6 md:p-8">
        <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6 text-center sm:text-left">
          <div className="w-20 h-20 rounded-full bg-[#58cc02] flex items-center justify-center text-black font-black text-4xl shadow-[0_4px_0_#46a302]">
            {user.display_name.charAt(0)}
          </div>
          <div className="space-y-1">
            <h1 className="text-2xl md:text-3xl font-extrabold text-white">
              {user.display_name}
            </h1>
            <p className="text-sm text-gray-400 font-medium">@{user.username}</p>
            <p className="text-xs text-gray-500">{user.email}</p>
          </div>
        </div>
      </Card>

      {/* Gamification Stats */}
      <div>
        <h2 className="text-lg font-bold text-gray-200 mb-3">Statistics</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Card className="text-center">
            <div className="text-2xl font-black text-[#ffc800]">{stats.total_xp}</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Total XP</div>
          </Card>
          <Card className="text-center">
            <div className="text-2xl font-black text-[#ff9600]">{stats.current_streak} Days</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Current Streak</div>
          </Card>
          <Card className="text-center">
            <div className="text-2xl font-black text-[#ff9600]">{stats.longest_streak} Days</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Longest Streak</div>
          </Card>
          <Card className="text-center">
            <div className="text-2xl font-black text-[#1cb0f6]">{stats.gems}</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Gems</div>
          </Card>
        </div>
      </div>

      {/* Achievements Section */}
      <div>
        <h2 className="text-lg font-bold text-gray-200 mb-3">Achievements</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {achievements.map((item) => (
            <Card
              key={item.achievement.id}
              className={`flex items-start gap-4 ${
                !item.is_earned ? "opacity-50 grayscale" : ""
              }`}
            >
              <div className="w-12 h-12 rounded-2xl bg-[#ffc800]/20 text-[#ffc800] flex items-center justify-center text-2xl shrink-0 font-bold">
                🏆
              </div>
              <div className="flex-1 space-y-1">
                <div className="flex justify-between items-start">
                  <h3 className="font-bold text-base text-white">
                    {item.achievement.name}
                  </h3>
                  {item.is_earned ? (
                    <Badge variant="green">Unlocked</Badge>
                  ) : (
                    <Badge variant="gray">Locked</Badge>
                  )}
                </div>
                <p className="text-xs text-gray-400">
                  {item.achievement.description}
                </p>
                {item.is_earned && item.earned_at && (
                  <p className="text-[10px] text-gray-500 font-mono pt-1">
                    Earned on {new Date(item.earned_at).toLocaleDateString()}
                  </p>
                )}
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
