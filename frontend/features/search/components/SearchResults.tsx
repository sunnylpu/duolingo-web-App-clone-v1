"use client";

import React from "react";
import { SearchResponse } from "@/services/search-service";
import { SearchResultCard } from "./SearchResultCard";
import { SearchEmptyState } from "./SearchEmptyState";

interface SearchResultsProps {
  data: SearchResponse | null;
  loading: boolean;
  query: string;
  onSuggestionClick?: (sug: string) => void;
  onItemSelect?: () => void;
}

export const SearchResults: React.FC<SearchResultsProps> = ({
  data,
  loading,
  query,
  onSuggestionClick,
  onItemSelect,
}) => {
  if (loading) {
    return (
      <div className="py-6 text-center text-xs font-black text-gray-400 animate-pulse flex items-center justify-center gap-2">
        <span className="animate-spin text-base">⚙️</span>
        <span>Searching curriculum...</span>
      </div>
    );
  }

  if (!query.trim()) return null;

  if (!data || data.results.length === 0) {
    return (
      <SearchEmptyState query={query} onSuggestionClick={onSuggestionClick} />
    );
  }

  return (
    <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
      <div className="text-[10px] font-black uppercase text-gray-400 tracking-wider px-1">
        Results for &quot;{data.query}&quot; ({data.total_results})
      </div>

      <div className="space-y-2">
        {data.results.map((item) => (
          <SearchResultCard key={`${item.type}_${item.id}`} item={item} onSelect={onItemSelect} />
        ))}
      </div>
    </div>
  );
};
