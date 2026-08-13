"use client";

import { useEffect, useState } from "react";
import { pathService } from "@/services/path-service";
import { PathResponse } from "@/types";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { ProgressBar } from "@/components/ui/ProgressBar";

export default function LearnPage() {
  const [path, setPath] = useState<PathResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadPath = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await pathService.getLearningPath();
      setPath(data);
    } catch (err: any) {
      setError(err?.message || "Failed to load learning path from backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPath();
  }, []);

  if (loading) {
    return <LoadingState message="Loading learning path..." fullPage />;
  }

  if (error || !path) {
    return (
      <ErrorState
        title="Learning Path Unavailable"
        message={error || "Could not retrieve course units and skills."}
        onRetry={loadPath}
      />
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge variant="green">Completed</Badge>;
      case "in_progress":
        return <Badge variant="blue">In Progress</Badge>;
      case "available":
        return <Badge variant="yellow">Available</Badge>;
      case "locked":
      default:
        return <Badge variant="gray">Locked</Badge>;
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Course Banner */}
      <Card className="bg-[#182830] border-2 border-[#1cb0f6] p-6">
        <div className="flex justify-between items-center">
          <div>
            <Badge variant="blue" className="mb-2">
              Active Course
            </Badge>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white">
              {path.course.name}
            </h1>
            <p className="text-xs text-gray-400 mt-1">
              {path.course.description || "Language learning course"}
            </p>
          </div>
          <div className="text-right font-mono text-xs text-gray-400">
            <div>{path.course.source_language.toUpperCase()} → {path.course.target_language.toUpperCase()}</div>
            <div className="text-[#1cb0f6] font-bold mt-1">
              {path.units.length} Units
            </div>
          </div>
        </div>
      </Card>

      {/* Units & Skills List */}
      <div className="space-y-6">
        {path.units.map((unit) => (
          <div key={unit.id} className="space-y-3">
            {/* Unit Header */}
            <div className="bg-[#182830] p-4 rounded-xl border border-[#37464f] flex justify-between items-center">
              <div>
                <h2 className="font-extrabold text-base text-gray-200">
                  {unit.title}
                </h2>
                {unit.description && (
                  <p className="text-xs text-gray-400 mt-0.5">
                    {unit.description}
                  </p>
                )}
              </div>
              <Badge variant="gray">Unit {unit.order_index}</Badge>
            </div>

            {/* Skills Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {unit.skills.map((skill) => (
                <Card
                  key={skill.id}
                  className={`space-y-3 ${
                    skill.status === "locked" ? "opacity-60" : ""
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-bold text-base text-white">
                        {skill.title}
                      </h3>
                      {skill.description && (
                        <p className="text-xs text-gray-400 mt-0.5">
                          {skill.description}
                        </p>
                      )}
                    </div>
                    {getStatusBadge(skill.status)}
                  </div>

                  <div className="flex justify-between items-center text-xs text-gray-400 font-bold pt-2 border-t border-[#37464f]">
                    <span>👑 Level {skill.crown_level}</span>
                    <span>⭐ {skill.xp_reward} XP</span>
                  </div>

                  <ProgressBar value={skill.completion_percent} height="h-2" />
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
