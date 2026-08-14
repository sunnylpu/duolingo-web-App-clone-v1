"use client";

import React, { useEffect, useState } from "react";
import { vocabularyService, VocabularyResponse } from "@/services/vocabulary-service";
import { VocabularyCard } from "./VocabularyCard";
import { Card } from "@/components/ui/Card";
import { LoadingState } from "@/components/feedback/LoadingState";
import { ErrorState } from "@/components/feedback/ErrorState";

interface VocabularyExplorerProps {
  initialCourseId?: string;
}

export const VocabularyExplorer: React.FC<VocabularyExplorerProps> = ({
  initialCourseId = "crs_english",
}) => {
  const [courseId, setCourseId] = useState<string>(initialCourseId);
  const [selectedTopic, setSelectedTopic] = useState<string>("All");
  const [selectedDifficulty, setSelectedDifficulty] = useState<number | undefined>(undefined);
  const [searchQuery, setSearchQuery] = useState<string>("");

  const [data, setData] = useState<VocabularyResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchVocab = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await vocabularyService.getVocabulary(
        courseId,
        selectedTopic,
        selectedDifficulty,
        searchQuery
      );
      setData(res);
    } catch (err: any) {
      setError(err?.message || "Failed to load course vocabulary.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVocab();
  }, [courseId, selectedTopic, selectedDifficulty, searchQuery]);

  return (
    <div className="space-y-6 max-w-4xl mx-auto py-2">
      {/* Header */}
      <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-black text-white uppercase tracking-wider flex items-center gap-2">
              <span>📚</span>
              <span>Vocabulary Explorer</span>
            </h1>
            <p className="text-xs text-gray-400 font-medium mt-0.5">
              Explore words, translations, phonetic pronunciations, and audio across course topics
            </p>
          </div>

          {/* Course Selector */}
          <div className="flex items-center gap-2 bg-[#131f24] p-1.5 rounded-xl border border-[#37464f]">
            <button
              onClick={() => {
                setCourseId("crs_english");
                setSelectedTopic("All");
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-black transition-all ${
                courseId === "crs_english"
                  ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              🇬🇧 English
            </button>
            <button
              onClick={() => {
                setCourseId("crs_spanish");
                setSelectedTopic("All");
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-black transition-all ${
                courseId === "crs_spanish"
                  ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              🇪🇸 Spanish
            </button>
            <button
              onClick={() => {
                setCourseId("crs_french");
                setSelectedTopic("All");
              }}
              className={`px-3 py-1.5 rounded-lg text-xs font-black transition-all ${
                courseId === "crs_french"
                  ? "bg-[#1cb0f6] text-black shadow-[0_2px_0_#1899d6]"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              🇫🇷 French
            </button>
          </div>
        </div>

        {/* Filters bar */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 border-t border-[#37464f]/60">
          {/* Search Query Filter */}
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search word or translation..."
              className="w-full px-3 py-2 bg-[#131f24] border border-[#37464f] focus:border-[#1cb0f6] rounded-xl text-xs font-semibold text-white placeholder-gray-400 focus:outline-none transition-all"
            />
          </div>

          {/* Topic Filter */}
          <select
            value={selectedTopic}
            onChange={(e) => setSelectedTopic(e.target.value)}
            className="w-full px-3 py-2 bg-[#131f24] border border-[#37464f] focus:border-[#1cb0f6] rounded-xl text-xs font-bold text-white focus:outline-none transition-all cursor-pointer"
          >
            <option value="All">All Topics</option>
            {data?.topics.map((top) => (
              <option key={top} value={top}>
                {top}
              </option>
            ))}
          </select>

          {/* Difficulty Filter */}
          <select
            value={selectedDifficulty === undefined ? "" : String(selectedDifficulty)}
            onChange={(e) =>
              setSelectedDifficulty(
                e.target.value === "" ? undefined : Number(e.target.value)
              )
            }
            className="w-full px-3 py-2 bg-[#131f24] border border-[#37464f] focus:border-[#1cb0f6] rounded-xl text-xs font-bold text-white focus:outline-none transition-all cursor-pointer"
          >
            <option value="">All Difficulties</option>
            <option value="1">Beginner (Level 1)</option>
            <option value="2">Intermediate (Level 2)</option>
            <option value="3">Advanced (Level 3)</option>
          </select>
        </div>
      </Card>

      {/* Main Content */}
      {loading ? (
        <LoadingState message="Loading vocabulary words..." />
      ) : error ? (
        <ErrorState
          title="Vocabulary Offline"
          message={error}
          onRetry={fetchVocab}
        />
      ) : !data || data.items.length === 0 ? (
        <Card className="p-8 text-center bg-[#182830] border-2 border-[#37464f] space-y-2">
          <div className="text-3xl">🔍</div>
          <h3 className="text-sm font-black text-white">No Vocabulary Words Found</h3>
          <p className="text-xs text-gray-400">
            Try adjusting your topic or difficulty filter to view words in this course catalog.
          </p>
        </Card>
      ) : (
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs font-bold text-gray-400 px-1">
            <span>
              CATALOG WORDS ({data.total_items} ITEMS)
            </span>
            <span>FILTER: {selectedTopic}</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {data.items.map((item) => (
              <VocabularyCard key={item.id} item={item} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
