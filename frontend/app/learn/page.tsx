"use client";

import { useEffect, useState } from "react";
import { pathService } from "@/services/path-service";
import { userService } from "@/services/user-service";
import { PathResponse, UserStats } from "@/types";
import { ErrorState } from "@/components/feedback/ErrorState";
import { LearningPath } from "@/features/path/LearningPath";

export default function LearnPage() {
  const [path, setPath] = useState<PathResponse | null>(null);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [pathRes, statsRes] = await Promise.all([
        pathService.getLearningPath(),
        userService.getUserStats().catch(() => null),
      ]);
      setPath(pathRes);
      setStats(statsRes);
    } catch (err: any) {
      setError(err?.message || "Failed to load learning path from backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto space-y-6 py-4 animate-pulse">
        {/* Skeleton Course Banner */}
        <div className="h-32 bg-[#182830] rounded-2xl border-2 border-[#37464f]" />
        {/* Skeleton Goal Widget */}
        <div className="h-16 bg-[#182830] rounded-2xl border-2 border-[#37464f]" />
        {/* Skeleton Unit Card */}
        <div className="h-24 bg-[#182830] rounded-2xl border-2 border-[#37464f]" />
        {/* Skeleton Skill Nodes */}
        <div className="flex flex-col items-center gap-6 py-4">
          <div className="w-20 h-20 rounded-full bg-[#182830] border-2 border-[#37464f]" />
          <div className="w-20 h-20 rounded-full bg-[#182830] border-2 border-[#37464f]" />
        </div>
      </div>
    );
  }

  if (error || !path) {
    return (
      <div className="py-8">
        <ErrorState
          title="Couldn't load your learning path."
          message={error || "Failed to establish connection to learning path endpoint."}
          onRetry={loadData}
        />
      </div>
    );
  }

  return (
    <LearningPath
      pathData={path}
      stats={stats}
      onStartLesson={(skillId) => {
        // Will trigger lesson player navigation in Phase 06
        console.log(`Ready to start lesson for skill: ${skillId}`);
      }}
    />
  );
}
