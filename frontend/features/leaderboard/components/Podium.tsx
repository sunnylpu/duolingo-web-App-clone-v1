import React from "react";
import { LeaderboardEntry } from "@/types";

interface PodiumProps {
  entries: LeaderboardEntry[];
}

export const Podium: React.FC<PodiumProps> = ({ entries }) => {
  if (entries.length < 3) return null;

  const first = entries.find((e) => e.rank === 1) || entries[0];
  const second = entries.find((e) => e.rank === 2) || entries[1];
  const third = entries.find((e) => e.rank === 3) || entries[2];

  return (
    <div className="grid grid-cols-3 gap-2 sm:gap-4 items-end justify-center pt-6 pb-2 max-w-lg mx-auto select-none">
      {/* 2nd Place - Silver (Left) */}
      <div className="flex flex-col items-center space-y-2">
        <div className="relative">
          <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-gradient-to-tr from-gray-400 to-gray-200 border-2 border-gray-300 flex items-center justify-center font-black text-black text-xl shadow-lg">
            {second.display_name.charAt(0)}
          </div>
          <span className="absolute -bottom-2 right-0 text-xl">🥈</span>
        </div>
        <div className="text-center">
          <div className="text-xs font-extrabold text-gray-200 truncate max-w-[90px]">
            {second.display_name}
          </div>
          <div className="text-[11px] font-black text-[#ffc800]">{second.xp} XP</div>
        </div>
        <div className="w-full h-20 sm:h-24 bg-[#182830] border-t-4 border-[#e5e5e5] rounded-t-xl flex items-center justify-center text-gray-300 font-black text-2xl shadow-inner">
          2
        </div>
      </div>

      {/* 1st Place - Gold (Center, Tall) */}
      <div className="flex flex-col items-center space-y-2">
        <div className="relative">
          <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-tr from-amber-500 to-yellow-300 border-4 border-[#ffc800] flex items-center justify-center font-black text-black text-2xl shadow-xl animate-bounce">
            {first.display_name.charAt(0)}
          </div>
          <span className="absolute -bottom-2 right-0 text-2xl">🥇</span>
        </div>
        <div className="text-center">
          <div className="text-sm font-black text-white truncate max-w-[100px]">
            {first.display_name}
          </div>
          <div className="text-xs font-black text-[#ffc800]">{first.xp} XP</div>
        </div>
        <div className="w-full h-28 sm:h-32 bg-[#ffc800]/20 border-t-4 border-[#ffc800] rounded-t-xl flex items-center justify-center text-[#ffc800] font-black text-3xl shadow-inner">
          1
        </div>
      </div>

      {/* 3rd Place - Bronze (Right) */}
      <div className="flex flex-col items-center space-y-2">
        <div className="relative">
          <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-gradient-to-tr from-amber-700 to-amber-500 border-2 border-amber-600 flex items-center justify-center font-black text-white text-xl shadow-lg">
            {third.display_name.charAt(0)}
          </div>
          <span className="absolute -bottom-2 right-0 text-xl">🥉</span>
        </div>
        <div className="text-center">
          <div className="text-xs font-extrabold text-gray-200 truncate max-w-[90px]">
            {third.display_name}
          </div>
          <div className="text-[11px] font-black text-[#ffc800]">{third.xp} XP</div>
        </div>
        <div className="w-full h-16 sm:h-20 bg-[#182830] border-t-4 border-[#cd7f32] rounded-t-xl flex items-center justify-center text-amber-500 font-black text-2xl shadow-inner">
          3
        </div>
      </div>
    </div>
  );
};
