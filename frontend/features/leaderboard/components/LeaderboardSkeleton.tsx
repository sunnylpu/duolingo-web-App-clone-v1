import React from "react";
import { Card } from "@/components/ui/Card";

export const LeaderboardSkeleton: React.FC = () => {
  return (
    <div className="space-y-3 animate-pulse">
      {[1, 2, 3, 4, 5].map((i) => (
        <Card key={i} className="p-4 bg-[#131f24] border border-[#37464f]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-6 h-6 bg-[#37464f] rounded-full" />
              <div className="w-10 h-10 bg-[#37464f] rounded-full" />
              <div className="space-y-2">
                <div className="w-24 h-4 bg-[#37464f] rounded" />
                <div className="w-16 h-3 bg-[#37464f] rounded" />
              </div>
            </div>
            <div className="w-16 h-5 bg-[#37464f] rounded" />
          </div>
        </Card>
      ))}
    </div>
  );
};
