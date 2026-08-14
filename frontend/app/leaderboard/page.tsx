"use client";

import { useEffect, useState } from "react";
import { leaderboardService } from "@/services/leaderboard-service";
import { LeaderboardResponse, LeaderboardPeriod } from "@/types";
import { LeaderboardTabs } from "@/features/leaderboard/components/LeaderboardTabs";
import { Podium } from "@/features/leaderboard/components/Podium";
import { LeaderboardRow } from "@/features/leaderboard/components/LeaderboardRow";
import { LeaderboardSkeleton } from "@/features/leaderboard/components/LeaderboardSkeleton";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export default function LeaderboardPage() {
  const [period, setPeriod] = useState<LeaderboardPeriod>("weekly");
  const [scope, setScope] = useState<"global" | "friends">("global");
  const [data, setData] = useState<LeaderboardResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchLeaderboard = async (selectedPeriod: LeaderboardPeriod, selectedScope: "global" | "friends") => {
    setLoading(true);
    setError(null);
    try {
      const res = await leaderboardService.getLeaderboard(selectedPeriod, 20, 0, selectedScope);
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load leaderboard standings.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaderboard(period, scope);
  }, [period, scope]);

  return (
    <div className="space-y-6 max-w-3xl mx-auto py-2">
      {/* Page Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-black text-white flex items-center justify-center gap-3">
          <span>🏆</span> Leaderboard Leagues
        </h1>
        <p className="text-xs text-gray-400 font-medium max-w-sm mx-auto">
          Compete with fellow learners and friends by completing daily lessons.
        </p>
      </div>

      {/* Scope Selector (Global vs Friends) */}
      <div className="flex justify-center gap-2">
        <button
          onClick={() => setScope("global")}
          className={`px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-all ${
            scope === "global"
              ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
              : "bg-[#182830] text-gray-400 border border-[#37464f] hover:text-white"
          }`}
        >
          🌐 Global League
        </button>
        <button
          onClick={() => setScope("friends")}
          className={`px-4 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-all ${
            scope === "friends"
              ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
              : "bg-[#182830] text-gray-400 border border-[#37464f] hover:text-white"
          }`}
        >
          👥 Friends Only
        </button>
      </div>

      {/* Period Selector Tabs */}
      <LeaderboardTabs activePeriod={period} onChange={setPeriod} />

      {/* Main Content Area */}
      {loading ? (
        <LeaderboardSkeleton />
      ) : error || !data ? (
        <ErrorState
          title="Leaderboard Offline"
          message={error || "Could not load standings."}
          onRetry={() => fetchLeaderboard(period, scope)}
        />
      ) : data.entries.length === 0 ? (
        <Card className="p-8 text-center bg-[#182830] border-2 border-[#37464f] space-y-3">
          <div className="text-4xl">🌟</div>
          <h3 className="text-lg font-black text-white">No Leaderboard Entries Yet</h3>
          <p className="text-xs text-gray-400">
            {scope === "friends"
              ? "None of your friends have completed lessons for this period yet. Follow more friends!"
              : "Be the first learner to complete a lesson and claim #1 rank!"}
          </p>
        </Card>
      ) : (
        <div className="space-y-6">
          {/* Top 3 Podium Presentation */}
          <Podium entries={data.entries} />

          {/* Full Participant Standings List */}
          <div className="space-y-2.5">
            <div className="flex items-center justify-between text-xs font-bold text-gray-400 px-1">
              <span>LEARNER STANDINGS ({data.total_participants} LEARNERS)</span>
              <span>XP SCORED</span>
            </div>

            {data.entries.map((entry) => (
              <LeaderboardRow key={entry.user_id} entry={entry} />
            ))}
          </div>

          {/* Sticky Learner Rank Bar if learner is available */}
          {data.current_user_rank && (
            <Card className="p-4 bg-[#182830] border-2 border-[#58cc02] flex items-center justify-between shadow-xl">
              <div className="flex items-center gap-3">
                <span className="text-2xl">🔥</span>
                <div>
                  <div className="text-xs text-gray-400 font-bold uppercase">Your Standing</div>
                  <div className="text-base font-black text-white">
                    Ranked #{data.current_user_rank} of {data.total_participants} ({scope})
                  </div>
                </div>
              </div>
              <Badge variant="green">ACTIVE LEAGUE</Badge>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
