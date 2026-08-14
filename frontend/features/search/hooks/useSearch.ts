"use client";

import { useState, useEffect } from "react";
import { searchService, SearchResponse } from "@/services/search-service";

export function useSearch(initialQuery = "", courseId?: string, debounceMs = 300) {
  const [query, setQuery] = useState<string>(initialQuery);
  const [data, setData] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const cleanQ = query.trim();
    if (!cleanQ) {
      setData(null);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    const handler = setTimeout(async () => {
      try {
        const res = await searchService.search(cleanQ, courseId);
        setData(res);
      } catch (err: any) {
        setError(err?.message || "Search query failed.");
      } finally {
        setLoading(false);
      }
    }, debounceMs);

    return () => clearTimeout(handler);
  }, [query, courseId, debounceMs]);

  return { query, setQuery, data, loading, error };
}
