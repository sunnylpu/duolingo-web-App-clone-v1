"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { pathService } from "@/services/path-service";
import { userService } from "@/services/user-service";
import { homeService, HomeDashboardResponse } from "@/services/home-service";
import { PathResponse, UserStats } from "@/types";
import { ErrorState } from "@/components/feedback/ErrorState";
import { LearningPath } from "@/features/path/LearningPath";
import {
  ContinueLearningCard,
  DailyGoalCard,
  StreakCard,
  HeartsCard,
  CourseHub,
  HomeSkeleton,
} from "@/features/home";

function LearnPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const courseId = searchParams.get("course") || undefined;

  const [path, setPath] = useState<PathResponse | null>(null);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [homeData, setHomeData] = useState<HomeDashboardResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [pathRes, statsRes, homeRes] = await Promise.all([
        pathService.getLearningPath(courseId),
        userService.getUserStats().catch(() => null),
        homeService.getHomeDashboard(courseId).catch(() => null),
      ]);
      setPath(pathRes);
      setStats(statsRes);
      setHomeData(homeRes);
    } catch (err: any) {
      setError(err?.message || "Failed to load learner dashboard from backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [courseId]);

  const handleSelectCourse = (selectedCourseId: string) => {
    router.push(`/learn?course=${encodeURIComponent(selectedCourseId)}`);
  };

  if (loading) {
    return <HomeSkeleton />;
  }

  if (error || !path) {
    return (
      <div className="py-8">
        <ErrorState
          title="Couldn't load your learning dashboard."
          message={error || "Failed to establish connection to learning dashboard endpoint."}
          onRetry={loadData}
        />
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-4xl mx-auto py-2">
      {/* 1. Continue Learning Hero Card */}
      {homeData?.continue_learning && (
        <ContinueLearningCard
          summary={homeData.continue_learning}
          courseName={path.course.name}
        />
      )}

      {/* 2. Gamification & Daily Goal Stats Grid */}
      {homeData && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <DailyGoalCard dailyGoal={homeData.daily_goal} />
          <StreakCard streak={homeData.streak} />
          <HeartsCard
            hearts={homeData.hearts}
            onPracticeClick={() => router.push("/learn")}
          />
        </div>
      )}

      {/* 3. Course Hub Selector */}
      {homeData?.courses && homeData.courses.length > 0 && (
        <CourseHub
          courses={homeData.courses}
          currentCourseId={path.course.id}
          onSelectCourse={handleSelectCourse}
        />
      )}

      {/* 4. Quick Actions Shortcut Bar */}
      <div className="flex items-center justify-between gap-3 p-3 bg-[#182830] border-2 border-[#37464f] rounded-2xl">
        <span className="text-xs font-black uppercase text-gray-400 tracking-wider">
          Quick Navigation
        </span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              if (path.recommended_skill_id) {
                const recommendedLessonId = path.recommended_lesson_id || "lsn_greetings_01";
                router.push(`/lesson/${recommendedLessonId}`);
              }
            }}
            className="px-3 py-1.5 rounded-xl bg-[#58cc02]/20 hover:bg-[#58cc02]/30 border border-[#58cc02]/30 text-xs font-black text-[#58cc02] transition-all"
          >
            ▶ Continue Lesson
          </button>
          <button
            onClick={() => router.push("/leaderboard")}
            className="px-3 py-1.5 rounded-xl bg-[#ffc800]/20 hover:bg-[#ffc800]/30 border border-[#ffc800]/30 text-xs font-black text-[#ffc800] transition-all"
          >
            🏆 Leaderboard
          </button>
          <button
            onClick={() => router.push("/profile")}
            className="px-3 py-1.5 rounded-xl bg-[#1cb0f6]/20 hover:bg-[#1cb0f6]/30 border border-[#1cb0f6]/30 text-xs font-black text-[#1cb0f6] transition-all"
          >
            👤 Profile
          </button>
        </div>
      </div>

      {/* 5. Interactive Vertical Learning Path */}
      <div className="pt-2">
        <h2 className="text-lg font-black text-white uppercase tracking-wider mb-4 flex items-center gap-2">
          <span>🗺️</span>
          <span>Learning Path</span>
        </h2>
        <LearningPath
          pathData={path}
          stats={stats}
          onStartLesson={(skillId) => {
            console.log(`Ready to start lesson for skill: ${skillId}`);
          }}
        />
      </div>
    </div>
  );
}

export default function LearnPage() {
  return (
    <Suspense fallback={<HomeSkeleton />}>
      <LearnPageContent />
    </Suspense>
  );
}
