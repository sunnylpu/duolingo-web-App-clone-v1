"use client";

import React from "react";
import { Card } from "@/components/ui/Card";

interface SystemHealthCardProps {
  system: {
    requests_total: number;
    errors_total: number;
    database_status: string;
    version: string;
    environment: string;
  };
}

export const SystemHealthCard: React.FC<SystemHealthCardProps> = ({ system }) => {
  const isHealthy = system.database_status === "healthy";

  return (
    <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-black text-white uppercase tracking-wider flex items-center gap-2">
          <span>🖥️</span>
          <span>System Health & Status</span>
        </h3>
        <span
          className={`text-xs font-black px-3 py-1 rounded-xl border flex items-center gap-1.5 ${
            isHealthy
              ? "bg-[#58cc02]/10 border-[#58cc02]/30 text-[#58cc02]"
              : "bg-[#ff4b4b]/10 border-[#ff4b4b]/30 text-[#ff4b4b]"
          }`}
        >
          <span className="w-2 h-2 rounded-full bg-current animate-pulse" />
          {isHealthy ? "Operational" : "Degraded"}
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
        <div className="p-3 bg-[#131f24] rounded-xl border border-[#37464f]">
          <span className="text-[10px] font-bold text-gray-400 uppercase">API Version</span>
          <p className="text-sm font-black text-white mt-0.5">{system.version}</p>
        </div>

        <div className="p-3 bg-[#131f24] rounded-xl border border-[#37464f]">
          <span className="text-[10px] font-bold text-gray-400 uppercase">Environment</span>
          <p className="text-sm font-black text-[#1cb0f6] capitalize mt-0.5">
            {system.environment}
          </p>
        </div>

        <div className="p-3 bg-[#131f24] rounded-xl border border-[#37464f]">
          <span className="text-[10px] font-bold text-gray-400 uppercase">Database</span>
          <p className="text-sm font-black text-[#58cc02] capitalize mt-0.5">
            {system.database_status}
          </p>
        </div>

        <div className="p-3 bg-[#131f24] rounded-xl border border-[#37464f]">
          <span className="text-[10px] font-bold text-gray-400 uppercase">Total Requests</span>
          <p className="text-sm font-black text-[#ffc800] mt-0.5">
            {system.requests_total.toLocaleString()}
          </p>
        </div>
      </div>
    </Card>
  );
};
