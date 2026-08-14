"use client";

import React, { useState, useRef, useEffect } from "react";
import { useSearch } from "../hooks/useSearch";
import { SearchResults } from "./SearchResults";

interface SearchBarProps {
  courseId?: string;
  placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  courseId,
  placeholder = "Search lessons, skills, topics...",
}) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const { query, setQuery, data, loading } = useSearch("", courseId, 300);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div ref={containerRef} className="relative w-full max-w-sm">
      <div className="relative flex items-center">
        <span className="absolute left-3 text-sm text-gray-400">🔍</span>
        <input
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder={placeholder}
          className="w-full pl-9 pr-8 py-1.5 bg-[#182830] border border-[#37464f] focus:border-[#1cb0f6] rounded-xl text-xs font-semibold text-white placeholder-gray-400 focus:outline-none transition-all"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-2 text-xs font-bold text-gray-400 hover:text-white"
          >
            ✕
          </button>
        )}
      </div>

      {isOpen && query.trim() && (
        <div className="absolute left-0 right-0 top-full mt-2 z-50 bg-[#131f24] border-2 border-[#37464f] rounded-2xl p-3 shadow-2xl">
          <SearchResults
            data={data}
            loading={loading}
            query={query}
            onSuggestionClick={(sug) => setQuery(sug)}
            onItemSelect={() => setIsOpen(false)}
          />
        </div>
      )}
    </div>
  );
};
