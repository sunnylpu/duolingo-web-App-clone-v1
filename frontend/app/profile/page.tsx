"use client";

import { useEffect, useState } from "react";
import { userService } from "@/services/user-service";
import { achievementService } from "@/services/achievement-service";
import { courseService } from "@/services/course-service";
import { UserProfile, UserAchievement, CourseSummary } from "@/types";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Card } from "@/components/ui/Card";
import { StreakDisplay } from "@/components/gamification/StreakDisplay";
import { DailyActivitySummary } from "@/components/gamification/DailyActivitySummary";
import { AchievementCard } from "@/features/achievements/components/AchievementCard";
import { CourseProgressCard } from "@/features/course";

export default function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [achievements, setAchievements] = useState<UserAchievement[]>([]);
  const [courses, setCourses] = useState<CourseSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    setLoading(true);
    setError(null);
    try {
      const [profileRes, achRes, coursesRes] = await Promise.all([
        userService.getUserProfile(),
        achievementService.getMyAchievements(),
        courseService.getCourses().catch(() => []),
      ]);
      setProfile(profileRes);
      setAchievements(achRes);
      setCourses(coursesRes);
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

  const { user, stats } = profile;

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

      {/* Cross-Course Learning Dashboard */}
      <div>
        <h2 className="text-lg font-bold text-gray-200 mb-3">Learning Progress Dashboard</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {courses.map((c) => (
            <CourseProgressCard key={c.id} course={c} />
          ))}
        </div>
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
