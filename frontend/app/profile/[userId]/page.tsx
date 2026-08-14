"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { socialService, PublicProfile } from "@/services/social-service";
import { Card } from "@/components/ui/Card";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { FollowButton } from "@/features/social/components/FollowButton";
import { StreakDisplay } from "@/components/gamification/StreakDisplay";

export default function PublicProfilePage() {
  const params = useParams();
  const router = useRouter();
  const userId = params.userId as string;

  const [profile, setProfile] = useState<PublicProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadProfile = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await socialService.getPublicProfile(userId);
      setProfile(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load learner profile.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (userId) {
      loadProfile();
    }
  }, [userId]);

  if (loading) {
    return <LoadingState message="Loading learner profile..." fullPage />;
  }

  if (error || !profile) {
    return (
      <ErrorState
        title="Profile Unavailable"
        message={error || "Learner profile not found."}
        onRetry={loadProfile}
      />
    );
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto py-2">
      {/* Profile Header */}
      <Card className="p-6 md:p-8 bg-[#182830] border-2 border-[#37464f]">
        <div className="flex flex-col sm:flex-row items-center sm:items-start justify-between gap-6 text-center sm:text-left">
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 rounded-full bg-[#58cc02] flex items-center justify-center text-black font-black text-4xl shadow-[0_4px_0_#46a302]">
              {profile.avatar || profile.display_name.charAt(0)}
            </div>
            <div className="space-y-1">
              <h1 className="text-2xl md:text-3xl font-extrabold text-white flex items-center justify-center sm:justify-start gap-3">
                <span>{profile.display_name}</span>
                <StreakDisplay currentStreak={profile.current_streak} />
              </h1>
              <p className="text-sm text-gray-400 font-medium">@{profile.username}</p>
              <div className="flex items-center gap-4 text-xs font-bold text-gray-400 pt-1">
                <span><strong className="text-white">{profile.following_count}</strong> Following</span>
                <span>•</span>
                <span><strong className="text-white">{profile.followers_count}</strong> Followers</span>
              </div>
            </div>
          </div>

          <FollowButton
            userId={profile.id}
            initialIsFollowing={profile.is_following}
            onToggle={loadProfile}
          />
        </div>
      </Card>

      {/* Stats Overview */}
      <div className="grid grid-cols-3 gap-4 text-center">
        <Card className="p-4 bg-[#182830] border-2 border-[#37464f]">
          <div className="text-2xl font-black text-[#ffc800]">⭐ {profile.total_xp}</div>
          <div className="text-xs text-gray-400 font-bold uppercase mt-1">Total XP</div>
        </Card>
        <Card className="p-4 bg-[#182830] border-2 border-[#37464f]">
          <div className="text-2xl font-black text-[#ff9600]">🔥 {profile.current_streak}d</div>
          <div className="text-xs text-gray-400 font-bold uppercase mt-1">Current Streak</div>
        </Card>
        <Card className="p-4 bg-[#182830] border-2 border-[#37464f]">
          <div className="text-2xl font-black text-[#ff9600]">🏆 {profile.longest_streak}d</div>
          <div className="text-xs text-gray-400 font-bold uppercase mt-1">Best Streak</div>
        </Card>
      </div>

      <div className="pt-2">
        <button
          onClick={() => router.back()}
          className="text-xs font-black text-[#1cb0f6] hover:underline uppercase tracking-wider"
        >
          ← Back
        </button>
      </div>
    </div>
  );
}
