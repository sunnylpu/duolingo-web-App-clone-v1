"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { userService } from "@/services/user-service";
import { UserStats } from "@/types";

export const Header: React.FC = () => {
  const pathname = usePathname();
  const [stats, setStats] = useState<UserStats | null>(null);

  useEffect(() => {
    userService
      .getUserStats()
      .then(setStats)
      .catch(() => {
        // Fallback gracefully
      });
  }, [pathname]);

  const navItems = [
    { label: "Learn", href: "/learn" },
    { label: "Leaderboard", href: "/leaderboard" },
    { label: "Profile", href: "/profile" },
    { label: "Settings", href: "/settings" },
  ];

  return (
    <header className="sticky top-0 z-40 bg-[#131f24]/90 backdrop-blur border-b border-[#37464f] px-4 md:px-8 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        {/* Brand Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-9 h-9 rounded-xl bg-[#58cc02] flex items-center justify-center text-black font-black text-xl shadow-[0_3px_0_#46a302] group-hover:scale-105 transition-transform">
            D
          </div>
          <span className="font-black text-xl tracking-tight text-white hidden sm:inline">
            Duolingo
          </span>
        </Link>

        {/* Desktop Navigation Bar */}
        <nav className="hidden md:flex items-center gap-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`px-4 py-2 rounded-xl font-extrabold text-sm transition-all ${
                  isActive
                    ? "bg-[#182830] text-[#1cb0f6] border-2 border-[#1cb0f6]"
                    : "text-gray-400 hover:text-white hover:bg-[#182830]/60"
                }`}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* User Stats Bar */}
        <div className="flex items-center gap-3 text-xs md:text-sm font-black select-none">
          {stats ? (
            <>
              {/* Streak */}
              <div
                className="flex items-center gap-1 px-2.5 py-1 rounded-xl bg-[#182830] border border-[#ff9600]/30 text-[#ff9600]"
                title="Current Streak"
              >
                <span>🔥</span>
                <span>{stats.current_streak}</span>
              </div>
              {/* Total XP */}
              <div
                className="flex items-center gap-1 px-2.5 py-1 rounded-xl bg-[#182830] border border-[#ffc800]/30 text-[#ffc800]"
                title="Total XP"
              >
                <span>⭐</span>
                <span>{stats.total_xp}</span>
              </div>
              {/* Hearts */}
              <div
                className="flex items-center gap-1 px-2.5 py-1 rounded-xl bg-[#182830] border border-[#ff4b4b]/30 text-[#ff4b4b]"
                title="Hearts Remaining"
              >
                <span>❤️</span>
                <span>{stats.hearts}</span>
              </div>
              {/* Gems */}
              <div
                className="flex items-center gap-1 px-2.5 py-1 rounded-xl bg-[#182830] border border-[#1cb0f6]/30 text-[#1cb0f6]"
                title="Gems Balance"
              >
                <span>💎</span>
                <span>{stats.gems}</span>
              </div>
            </>
          ) : (
            <div className="text-xs text-gray-500 font-mono animate-pulse">
              Connecting...
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
