"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { userService } from "@/services/user-service";
import { User, UserStats } from "@/types";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Badge } from "@/components/ui/Badge";

export default function HomePage() {
  const [user, setUser] = useState<User | null>(null);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboard = async () => {
    setLoading(true);
    setError(null);
    try {
      const [userRes, statsRes] = await Promise.all([
        userService.getCurrentUser(),
        userService.getUserStats(),
      ]);
      setUser(userRes);
      setStats(statsRes);
    } catch (err: any) {
      setError(err?.message || "Failed to load user profile from backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return <LoadingState message="Loading dashboard data..." fullPage />;
  }

  if (error || !user || !stats) {
    return (
      <ErrorState
        title="Backend Connection Failed"
        message={error || "Could not retrieve user context."}
        onRetry={loadDashboard}
      />
    );
  }

  const dailyGoalPercent = Math.min(
    100,
    Math.round((stats.daily_xp / stats.daily_goal_xp) * 100)
  );

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Hero Welcome Card */}
      <Card className="relative overflow-hidden border-2 border-[#37464f] p-6 md:p-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-2xl bg-[#58cc02] flex items-center justify-center text-black font-black text-3xl shadow-[0_4px_0_#46a302]">
              {user.display_name.charAt(0)}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight">
                  Welcome back, {user.display_name}!
                </h1>
                <Badge variant="green">Learner</Badge>
              </div>
              <p className="text-sm text-gray-400 font-medium">@{user.username}</p>
            </div>
          </div>

          <Link href="/learn">
            <Button variant="primary" size="lg" className="w-full md:w-auto">
              Continue Learning →
            </Button>
          </Link>
        </div>
      </Card>

      {/* Stats Overview Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {/* Streak */}
        <Card className="text-center space-y-1">
          <div className="text-3xl">🔥</div>
          <div className="text-xl font-black text-[#ff9600]">
            {stats.current_streak} Days
          </div>
          <div className="text-xs text-gray-400 font-bold uppercase tracking-wider">
            Current Streak
          </div>
        </Card>

        {/* Total XP */}
        <Card className="text-center space-y-1">
          <div className="text-3xl">⭐</div>
          <div className="text-xl font-black text-[#ffc800]">
            {stats.total_xp} XP
          </div>
          <div className="text-xs text-gray-400 font-bold uppercase tracking-wider">
            Total Earned
          </div>
        </Card>

        {/* Hearts */}
        <Card className="text-center space-y-1">
          <div className="text-3xl">❤️</div>
          <div className="text-xl font-black text-[#ff4b4b]">
            {stats.hearts} / 5
          </div>
          <div className="text-xs text-gray-400 font-bold uppercase tracking-wider">
            Hearts Remaining
          </div>
        </Card>

        {/* Gems */}
        <Card className="text-center space-y-1">
          <div className="text-3xl">💎</div>
          <div className="text-xl font-black text-[#1cb0f6]">
            {stats.gems}
          </div>
          <div className="text-xs text-gray-400 font-bold uppercase tracking-wider">
            Gems Balance
          </div>
        </Card>
      </div>

      {/* Daily Progress Goal */}
      <Card className="space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h3 className="font-extrabold text-base text-gray-200">
              Daily XP Goal
            </h3>
            <p className="text-xs text-gray-400">
              {stats.daily_xp} of {stats.daily_goal_xp} XP earned today
            </p>
          </div>
          <Badge variant={dailyGoalPercent >= 100 ? "green" : "yellow"}>
            {dailyGoalPercent >= 100 ? "Goal Reached!" : `${dailyGoalPercent}%`}
          </Badge>
        </div>
        <ProgressBar value={dailyGoalPercent} height="h-4" />
      </Card>
    </div>
  );
}
