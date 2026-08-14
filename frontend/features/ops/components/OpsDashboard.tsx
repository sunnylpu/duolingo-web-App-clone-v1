"use client";

import React from "react";
import { useOpsOverview } from "../hooks/useOpsOverview";
import { SystemHealthCard } from "./SystemHealthCard";
import { MetricCard } from "./MetricCard";
import { ErrorState } from "@/components/feedback/ErrorState";

export const OpsDashboard: React.FC = () => {
  const { data, loading, error, refresh } = useOpsOverview();

  if (loading && !data) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-28 bg-[#182830] border-2 border-[#37464f] rounded-2xl" />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="h-24 bg-[#182830] rounded-2xl" />
          <div className="h-24 bg-[#182830] rounded-2xl" />
          <div className="h-24 bg-[#182830] rounded-2xl" />
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <ErrorState
        title="Could not load operations metrics"
        message={error || "Failed to establish connection to operations telemetry API."}
        onRetry={refresh}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-black text-white uppercase tracking-wider flex items-center gap-2">
            <span>⚙️</span>
            <span>Operations & Observability</span>
          </h1>
          <p className="text-xs text-gray-400 font-medium mt-0.5">
            Real-time business telemetry, system health, and request correlation
          </p>
        </div>

        <button
          onClick={refresh}
          className="px-3 py-1.5 rounded-xl bg-[#182830] hover:bg-[#203038] border border-[#37464f] text-xs font-black text-white transition-all flex items-center gap-1.5"
        >
          <span>🔄</span>
          <span>Refresh</span>
        </button>
      </div>

      {/* System Health Overview Card */}
      <SystemHealthCard system={data.system} />

      {/* Business Telemetry Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <MetricCard
          title="Active Users Today"
          value={data.users.active_today}
          subtitle={`Total learners: ${data.users.total}`}
          icon="👥"
          color="blue"
        />

        <MetricCard
          title="Lessons Completed Today"
          value={data.learning.lessons_completed_today}
          subtitle={`Total courses: ${data.courses.total}`}
          icon="📚"
          color="green"
        />

        <MetricCard
          title="Exercise Accuracy"
          value={`${data.learning.correct_answer_pct}%`}
          subtitle={`Exercises: ${data.learning.exercises_answered_today}`}
          icon="🎯"
          color="purple"
        />

        <MetricCard
          title="XP Awarded Today"
          value={`+${data.gamification.xp_awarded_today.toLocaleString()}`}
          subtitle="From lessons & practice"
          icon="⭐"
          color="yellow"
        />

        <MetricCard
          title="Achievements Unlocked Today"
          value={data.gamification.achievements_unlocked_today}
          subtitle="Unlocked by active learners"
          icon="🏆"
          color="yellow"
        />

        <MetricCard
          title="API Error Count"
          value={data.system.errors_total}
          subtitle={`Requests total: ${data.system.requests_total}`}
          icon="🚨"
          color={data.system.errors_total > 0 ? "red" : "green"}
        />
      </div>
    </div>
  );
};
