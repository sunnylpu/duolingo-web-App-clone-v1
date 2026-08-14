"use client";

import React from "react";

export const HomeSkeleton: React.FC = () => {
  return (
    <div className="space-y-8 animate-pulse max-w-4xl mx-auto py-2">
      {/* Hero Continue Card Skeleton */}
      <div className="h-44 bg-[#182830] border-2 border-[#37464f] rounded-2xl p-6 flex flex-col justify-between">
        <div className="space-y-3">
          <div className="h-4 w-32 bg-[#37464f] rounded-full" />
          <div className="h-8 w-64 bg-[#37464f] rounded-xl" />
          <div className="h-3 w-96 bg-[#37464f] rounded-full" />
        </div>
        <div className="h-3 w-full bg-[#37464f] rounded-full" />
      </div>

      {/* Daily Goal & Stats Grid Skeleton */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="h-28 bg-[#182830] border-2 border-[#37464f] rounded-2xl p-5" />
        <div className="h-28 bg-[#182830] border-2 border-[#37464f] rounded-2xl p-5" />
        <div className="h-28 bg-[#182830] border-2 border-[#37464f] rounded-2xl p-5" />
      </div>

      {/* Course Hub Skeleton */}
      <div className="space-y-3">
        <div className="h-6 w-36 bg-[#37464f] rounded-full" />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="h-36 bg-[#182830] border-2 border-[#37464f] rounded-2xl p-4" />
          <div className="h-36 bg-[#182830] border-2 border-[#37464f] rounded-2xl p-4" />
          <div className="h-36 bg-[#182830] border-2 border-[#37464f] rounded-2xl p-4" />
        </div>
      </div>
    </div>
  );
};
