"use client";

import { useEffect, useState } from "react";
import { userService } from "@/services/user-service";
import { achievementService } from "@/services/achievement-service";
import { UserProfile, UserAchievement } from "@/types";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Card } from "@/components/ui/Card";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { StreakDisplay } from "@/components/gamification/StreakDisplay";
import { DailyActivitySummary } from "@/components/gamification/DailyActivitySummary";
import { AchievementCard } from "@/features/achievements/components/AchievementCard";

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [achievements, setAchievements] = useState<UserAchievement[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    setLoading(true);
    setError(null);
    try {
      const [profileRes, achRes] = await Promise.all([
        userService.getUserProfile(),
        achievementService.getMyAchievements(),
      ]);
      setProfile(profileRes);
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
    return <LoadingState message="Loading profile dashboard..." fullPage />;
  }

  if (error || !profile) {
    return (
      <ErrorState
        title="Profile Unavailable"
        message={error || "Could not retrieve user profile."}
        onRetry={loadProfile}
      />
    );
  }

  const { user, stats, learning } = profile;

  return (
    <div className="space-y-8 max-w-4xl mx-auto py-2">
      {/* Profile Header Card */}
      <Card className="p-6 md:p-8 bg-[#182830] border-2 border-[#37464f]">
        <div className="flex flex-col sm:flex-row items-center sm:items-start justify-between gap-6 text-center sm:text-left">
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 rounded-full bg-[#58cc02] flex items-center justify-center text-black font-black text-4xl shadow-[0_4px_0_#46a302]">
              {user.display_name.charAt(0)}
            </div>
            <div className="space-y-1">
              <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center justify-center sm:justify-start gap-3">
                <span>{user.display_name}</span>
                <StreakDisplay currentStreak={stats.current_streak} />
              </h1>
              <p className="text-sm text-gray-400 font-medium">@{user.username}</p>
              <p className="text-xs text-gray-500">{user.email}</p>
            </div>
          </div>
        </div>
      </Card>

      {/* Gamification Statistics Grid */}
      <div>
        <h2 className="text-lg font-bold text-gray-200 mb-3">Statistics</h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <Card className="text-center p-4 bg-[#182830] border-2 border-[#37464f]">
            <div className="text-2xl font-black text-[#ffc800]">⭐ {stats.total_xp}</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Total XP</div>
          </Card>
          <Card className="text-center p-4 bg-[#182830] border-2 border-[#37464f]">
            <div className="text-2xl font-black text-[#ff9600]">🔥 {stats.current_streak}d</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Current Streak</div>
          </Card>
          <Card className="text-center p-4 bg-[#182830] border-2 border-[#37464f]">
            <div className="text-2xl font-black text-[#ff9600]">🏆 {stats.longest_streak}d</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Longest Streak</div>
          </Card>
          <Card className="text-center p-4 bg-[#182830] border-2 border-[#37464f]">
            <div className="text-2xl font-black text-[#1cb0f6]">💎 {stats.gems}</div>
            <div className="text-xs text-gray-400 font-bold uppercase mt-1">Gems</div>
          </Card>
        </div>
      </div>

      {/* Learning Progress Summary */}
      <div>
        <h2 className="text-lg font-bold text-gray-200 mb-3">Course Progress Summary</h2>
        <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-4">
          <div className="grid grid-cols-3 gap-3 text-center">
            <div className="p-3 bg-[#131f24] rounded-2xl border border-[#37464f]">
              <div className="text-xs text-gray-400 font-bold uppercase">Lessons Done</div>
              <div className="text-xl font-black text-[#1cb0f6] mt-1">📚 {learning.lessons_completed}</div>
            </div>
            <div className="p-3 bg-[#131f24] rounded-2xl border border-[#37464f]">
              <div className="text-xs text-gray-400 font-bold uppercase">Skills Mastered</div>
              <div className="text-xl font-black text-[#58cc02] mt-1">👑 {learning.skills_completed}</div>
            </div>
            <div className="p-3 bg-[#131f24] rounded-2xl border border-[#37464f]">
              <div className="text-xs text-gray-400 font-bold uppercase">In Progress</div>
              <div className="text-xl font-black text-[#ffc800] mt-1">📖 {learning.skills_in_progress}</div>
            </div>
          </div>

          <div className="space-y-2 pt-2">
            <div className="flex justify-between items-center text-xs font-black">
              <span className="text-gray-300 uppercase tracking-wider">Overall Spanish Progress</span>
              <span className="text-[#58cc02]">{learning.course_progress_percent}%</span>
            </div>
            <ProgressBar value={learning.course_progress_percent} height="h-3.5" />
          </div>
        </Card>
      </div>

      {/* Today's Daily Activity Widget */}
      <DailyActivitySummary
        xpEarned={stats.daily_xp || 0}
        lessonsCompleted={stats.daily_xp ? Math.ceil(stats.daily_xp / 10) : 0}
        goalXp={stats.daily_goal_xp}
        goalCompleted={Boolean(stats.daily_goal_completed || (stats.daily_xp >= stats.daily_goal_xp))}
      />

      {/* Achievements Section */}
      <div>
        <h2 className="text-lg font-bold text-gray-200 mb-3">Achievements</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {achievements.map((item) => (
            <AchievementCard key={item.achievement.id} userAchievement={item} />
          ))}
        </div>
      </div>
    </div>
  );
}
