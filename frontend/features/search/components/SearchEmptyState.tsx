"use client";

import React from "react";

interface SearchEmptyStateProps {
  query: string;
  onSuggestionClick?: (suggestion: string) => void;
}

export const SearchEmptyState: React.FC<SearchEmptyStateProps> = ({
  query,
  onSuggestionClick,
}) => {
  const suggestions = ["Food", "Travel", "Greetings", "Basics", "Restaurant"];

  return (
    <div className="p-6 bg-[#182830] border-2 border-[#37464f] rounded-2xl text-center space-y-3">
      <div className="text-3xl">🔍</div>
      <h4 className="text-sm font-black text-white">
        No results for &quot;{query}&quot;
      </h4>
      <p className="text-xs text-gray-400 max-w-xs mx-auto">
        Try searching for popular course topics or skills:
      </p>

      <div className="flex flex-wrap items-center justify-center gap-1.5 pt-1">
        {suggestions.map((sug) => (
          <button
            key={sug}
            onClick={() => onSuggestionClick && onSuggestionClick(sug)}
            className="px-2.5 py-1 bg-[#131f24] hover:bg-[#1cb0f6]/20 border border-[#37464f] hover:border-[#1cb0f6] text-[#1cb0f6] text-xs font-bold rounded-lg transition-all"
          >
            {sug}
          </button>
        ))}
      </div>
    </div>
  );
};
