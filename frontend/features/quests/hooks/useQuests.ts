"use client";

import { useState, useEffect } from "react";
import { questService, DailyQuestsResponse, WeeklyChallengeResponse } from "@/services/quest-service";

export function useQuests() {
  const [dailyData, setDailyData] = useState<DailyQuestsResponse | null>(null);
  const [weeklyData, setWeeklyData] = useState<WeeklyChallengeResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchQuests = async () => {
    setLoading(true);
    setError(null);
    try {
      const [dailyRes, weeklyRes] = await Promise.all([
        questService.getTodayQuests().catch(() => ({ date: "", user_id: "", quests: [] })),
        questService.getWeeklyChallenge().catch(() => ({ week_start_date: "", challenge: null })),
      ]);
      setDailyData(dailyRes);
      setWeeklyData(weeklyRes);
    } catch (err: any) {
      setError(err?.message || "Failed to load active quests.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQuests();
  }, []);

  return { dailyData, weeklyData, loading, error, refresh: fetchQuests };
}
