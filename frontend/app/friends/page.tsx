"use client";

import { useEffect, useState } from "react";
import {
  socialService,
  UserSocialSummary,
  ActivityEvent,
  FriendSuggestion,
  SocialStats,
} from "@/services/social-service";
import { Card } from "@/components/ui/Card";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { FriendCard } from "@/features/social/components/FriendCard";
import { SocialFeed } from "@/features/social/components/SocialFeed";
import { FriendSuggestions } from "@/features/social/components/FriendSuggestions";

export default function FriendsPage() {
  const [tab, setTab] = useState<"following" | "followers" | "feed">("feed");
  const [stats, setStats] = useState<SocialStats | null>(null);
  const [following, setFollowing] = useState<UserSocialSummary[]>([]);
  const [followers, setFollowers] = useState<UserSocialSummary[]>([]);
  const [suggestions, setSuggestions] = useState<FriendSuggestion[]>([]);
  const [feed, setFeed] = useState<ActivityEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [statsRes, followingRes, followersRes, suggRes, feedRes] = await Promise.all([
        socialService.getSocialStats().catch(() => ({ followers_count: 0, following_count: 0 })),
        socialService.getFollowing().catch(() => []),
        socialService.getFollowers().catch(() => []),
        socialService.getSuggestions().catch(() => []),
        socialService.getFeed().catch(() => ({ items: [], total: 0 })),
      ]);
      setStats(statsRes);
      setFollowing(followingRes);
      setFollowers(followersRes);
      setSuggestions(suggRes);
      setFeed(feedRes.items);
    } catch (err: any) {
      setError(err?.message || "Failed to load social learning dashboard.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return <LoadingState message="Loading social network..." fullPage />;
  }

  if (error) {
    return (
      <ErrorState
        title="Social Network Unavailable"
        message={error}
        onRetry={loadData}
      />
    );
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto py-2">
      {/* Social Header */}
      <Card className="p-6 bg-[#182830] border-2 border-[#37464f]">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-black text-white uppercase tracking-wider flex items-center gap-2">
              <span>👥</span>
              <span>Friends & Social Activity</span>
            </h1>
            <p className="text-xs text-gray-400 font-medium mt-0.5">
              Connect with fellow learners, follow progress, and compete on friend leaderboards
            </p>
          </div>

          <div className="flex items-center gap-3 bg-[#131f24] px-4 py-2 rounded-xl border border-[#37464f] text-xs font-black">
            <div>
              <span className="text-gray-400 block text-[10px] uppercase">Following</span>
              <span className="text-[#1cb0f6] text-sm">{stats?.following_count || 0}</span>
            </div>
            <div className="h-6 w-px bg-[#37464f]" />
            <div>
              <span className="text-gray-400 block text-[10px] uppercase">Followers</span>
              <span className="text-[#58cc02] text-sm">{stats?.followers_count || 0}</span>
            </div>
          </div>
        </div>
      </Card>

      {/* Tabs */}
      <div className="flex items-center gap-2 border-b border-[#37464f] pb-3">
        <button
          onClick={() => setTab("feed")}
          className={`px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-all ${
            tab === "feed"
              ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
              : "bg-[#182830] text-gray-400 border border-[#37464f] hover:text-white"
          }`}
        >
          ⚡ Activity Feed
        </button>
        <button
          onClick={() => setTab("following")}
          className={`px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-all ${
            tab === "following"
              ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
              : "bg-[#182830] text-gray-400 border border-[#37464f] hover:text-white"
          }`}
        >
          Following ({following.length})
        </button>
        <button
          onClick={() => setTab("followers")}
          className={`px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-all ${
            tab === "followers"
              ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
              : "bg-[#182830] text-gray-400 border border-[#37464f] hover:text-white"
          }`}
        >
          Followers ({followers.length})
        </button>
      </div>

      {/* Tab Contents */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 space-y-4">
          {tab === "feed" && <SocialFeed items={feed} />}

          {tab === "following" && (
            <div className="space-y-3">
              {following.length === 0 ? (
                <div className="p-6 bg-[#182830] border-2 border-[#37464f] rounded-2xl text-center text-xs font-medium text-gray-400">
                  You are not following any learners yet. Check suggestions to get started!
                </div>
              ) : (
                following.map((u) => (
                  <FriendCard key={u.id} user={u} onFollowToggle={loadData} />
                ))
              )}
            </div>
          )}

          {tab === "followers" && (
            <div className="space-y-3">
              {followers.length === 0 ? (
                <div className="p-6 bg-[#182830] border-2 border-[#37464f] rounded-2xl text-center text-xs font-medium text-gray-400">
                  No followers yet. Keep practicing to build your profile presence!
                </div>
              ) : (
                followers.map((u) => (
                  <FriendCard key={u.id} user={u} onFollowToggle={loadData} />
                ))
              )}
            </div>
          )}
        </div>

        {/* Sidebar: Suggestions */}
        <div>
          <FriendSuggestions suggestions={suggestions} onRefresh={loadData} />
        </div>
      </div>
    </div>
  );
}
