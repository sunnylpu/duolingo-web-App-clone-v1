"use client";

import { useState, useEffect, useCallback } from "react";
import { opsService, OpsOverviewResponse } from "@/services/ops-service";

export function useOpsOverview() {
  const [data, setData] = useState<OpsOverviewResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchOverview = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await opsService.getOverview();
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load operational telemetry metrics.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchOverview();
    const interval = setInterval(fetchOverview, 10000); // 10s auto-refresh
    return () => clearInterval(interval);
  }, [fetchOverview]);

  return { data, loading, error, refresh: fetchOverview };
}
