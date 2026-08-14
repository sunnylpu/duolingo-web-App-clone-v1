"use client";

import React from "react";
import { VocabularyItem } from "@/services/vocabulary-service";
import { AudioButton } from "@/features/audio/components/AudioButton";

interface VocabularyCardProps {
  item: VocabularyItem;
}

const DIFFICULTY_LABELS: Record<number, { label: string; color: string }> = {
  1: { label: "Beginner", color: "text-[#58cc02] border-[#58cc02]/30" },
  2: { label: "Intermediate", color: "text-[#ffc800] border-[#ffc800]/30" },
  3: { label: "Advanced", color: "text-[#ff9600] border-[#ff9600]/30" },
};

export const VocabularyCard: React.FC<VocabularyCardProps> = ({ item }) => {
  const diffInfo = DIFFICULTY_LABELS[item.difficulty] || DIFFICULTY_LABELS[1];

  // Map course language code to BCP 47 tag for speech synthesis
  const langCode = item.course_id === "crs_spanish" ? "es-ES" : item.course_id === "crs_french" ? "fr-FR" : "en-US";

  return (
    <div className="p-4 bg-[#182830] border-2 border-[#37464f] rounded-2xl flex flex-col justify-between space-y-3 shadow-md hover:border-[#1cb0f6] transition-all">
      <div className="flex items-start justify-between gap-2">
        <div>
          <span className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded bg-[#131f24] text-[#1cb0f6] border border-[#37464f]">
            {item.topic}
          </span>
          <h3 className="text-lg font-black text-white mt-1.5 flex items-center gap-2">
            <span>{item.word}</span>
          </h3>
          {item.phonetic && (
            <p className="text-xs font-mono text-gray-400 mt-0.5">{item.phonetic}</p>
          )}
        </div>

        <span className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-[#131f24] border ${diffInfo.color}`}>
          {diffInfo.label}
        </span>
      </div>

      <div className="pt-2 border-t border-[#37464f]/60 flex items-center justify-between gap-2">
        <div>
          <span className="text-[10px] font-bold text-gray-400 block uppercase">Translation</span>
          <span className="text-sm font-extrabold text-[#58cc02]">{item.translation}</span>
        </div>

        <AudioButton text={item.word} lang={langCode} size="sm" />
      </div>
    </div>
  );
};
