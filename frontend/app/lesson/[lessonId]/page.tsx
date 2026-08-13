"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { lessonService } from "@/services/lesson-service";
import { userService } from "@/services/user-service";
import { LessonDetail, UserStats } from "@/types";
import { ErrorState } from "@/components/feedback/ErrorState";
import { LessonLoading } from "@/features/lesson/components/LessonLoading";
import { LessonPlayer } from "@/features/lesson/components/LessonPlayer";
import { Button } from "@/components/ui/Button";

export default function LessonPage() {
  const params = useParams();
  const lessonId = params?.lessonId as string;

  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [stats, setStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadLesson = async () => {
    if (!lessonId) return;
    setLoading(true);
    setError(null);

    try {
      const [lessonRes, statsRes] = await Promise.all([
        lessonService.getLesson(lessonId),
        userService.getUserStats().catch(() => null),
      ]);
      setLesson(lessonRes);
      setStats(statsRes);
    } catch (err: any) {
      setError(err?.message || "Failed to retrieve lesson content from backend.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLesson();
  }, [lessonId]);

  if (loading) {
    return <LessonLoading />;
  }

  if (error || !lesson) {
    return (
      <div className="max-w-md mx-auto py-12 px-4 space-y-4">
        <ErrorState
          title="Couldn't load this lesson."
          message={error || "Lesson not found or backend unreachable."}
          onRetry={loadLesson}
        />
        <div className="text-center">
          <Button
            variant="outline"
            onClick={() => {
              window.location.href = "/learn";
            }}
          >
            ← BACK TO PATH
          </Button>
        </div>
      </div>
    );
  }

  return <LessonPlayer lesson={lesson} stats={stats} />;
}
