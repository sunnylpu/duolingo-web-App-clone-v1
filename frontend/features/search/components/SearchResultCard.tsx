"use client";

import React from "react";
import Link from "next/link";
import { SearchResultItem } from "@/services/search-service";

interface SearchResultCardProps {
  item: SearchResultItem;
  onSelect?: () => void;
}

const TYPE_ICONS: Record<string, string> = {
  course: "🎓",
  unit: "👑",
  skill: "🔮",
  lesson: "⚡",
  vocabulary: "🍎",
};

export const SearchResultCard: React.FC<SearchResultCardProps> = ({ item, onSelect }) => {
  const icon = TYPE_ICONS[item.type] || "📖";
  const isLocked = item.status === "locked";

  let href = "/learn";
  if (item.type === "lesson" && item.id) {
    href = `/lesson/${item.id}`;
  }

  return (
    <Link
      href={href}
      onClick={(e) => {
        if (isLocked && item.type === "lesson") {
          e.preventDefault();
          alert("This lesson is locked. Complete the prerequisite skill first!");
          return;
        }
        if (onSelect) onSelect();
      }}
      className={`p-3.5 bg-[#182830] border-2 border-[#37464f] rounded-2xl flex items-center justify-between gap-3 transition-all hover:border-[#1cb0f6] group ${
        isLocked ? "opacity-75" : ""
      }`}
    >
      <div className="flex items-center gap-3 min-w-0">
        <div className="w-9 h-9 rounded-xl bg-[#131f24] border border-[#37464f] flex items-center justify-center text-lg shrink-0 group-hover:scale-105 transition-transform">
          {icon}
        </div>
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <h4 className="text-xs font-black text-white group-hover:text-[#1cb0f6] transition-colors truncate">
              {item.title}
            </h4>
            <span className="text-[9px] font-black uppercase tracking-wider px-1.5 py-0.5 rounded bg-[#131f24] text-gray-400 border border-[#37464f]">
              {item.type}
            </span>
          </div>
          {item.description && (
            <p className="text-[11px] text-gray-400 font-medium truncate mt-0.5">
              {item.description}
            </p>
          )}
        </div>
      </div>

      <div className="shrink-0 text-right">
        {isLocked ? (
          <span className="text-xs font-bold text-gray-500 flex items-center gap-1">
            🔒 Locked
          </span>
        ) : item.status === "completed" ? (
          <span className="text-xs font-bold text-[#58cc02] flex items-center gap-1">
            ✓ Done
          </span>
        ) : (
          <span className="text-xs font-bold text-[#1cb0f6]">View →</span>
        )}
      </div>
    </Link>
  );
};
