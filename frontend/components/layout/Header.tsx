"use client";

import React, { useEffect, useState, Suspense } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { userService } from "@/services/user-service";
import { UserStats } from "@/types";
import { OutOfHeartsModal } from "@/features/gamification/components/OutOfHeartsModal";
import { CourseSwitcher } from "@/features/course";
import { SearchBar } from "@/features/search";
import { NotificationBell } from "@/features/notifications";

export const Header: React.FC = () => {
  const pathname = usePathname();
  const [stats, setStats] = useState<UserStats | null>(null);
  const [showHeartModal, setShowHeartModal] = useState<boolean>(false);

  const fetchStats = () => {
    userService
      .getUserStats()
      .then(setStats)
      .catch(() => {
        // Fallback gracefully
      });
  };

  useEffect(() => {
    fetchStats();
  }, [pathname]);

  const navItems = [
    { label: "Learn", href: "/learn" },
    { label: "Vocab", href: "/vocabulary" },
    { label: "Friends", href: "/friends" },
    { label: "Leaderboard", href: "/leaderboard" },
    { label: "Profile", href: "/profile" },
  ];

  return (
    <>
      <header className="sticky top-0 z-40 bg-[#131f24]/90 backdrop-blur border-b border-[#37464f] px-4 md:px-8 py-3">
        <div className="max-w-6xl mx-auto flex items-center justify-between gap-4">
          {/* Brand Logo & Course Selector */}
          <div className="flex items-center gap-3 shrink-0">
            <Link href="/" className="flex items-center gap-2 group">
              <div className="w-9 h-9 rounded-xl bg-[#58cc02] flex items-center justify-center text-black font-black text-xl shadow-[0_3px_0_#46a302] group-hover:scale-105 transition-transform">
                D
              </div>
              <span className="font-black text-xl tracking-tight text-white hidden lg:inline">
                Duolingo
              </span>
            </Link>

            <Suspense fallback={<div className="w-24 h-8 bg-slate-800 rounded-xl animate-pulse" />}>
              <CourseSwitcher />
            </Suspense>
          </div>

          {/* Search Bar Widget */}
          <div className="hidden sm:block flex-1 max-w-xs">
            <SearchBar />
          </div>

          {/* Desktop Navigation Bar */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`px-3 py-1.5 rounded-xl font-extrabold text-xs lg:text-sm transition-all ${
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

          {/* Notification Bell & User Stats Bar */}
          <div className="flex items-center gap-2 text-xs font-black select-none shrink-0">
            <NotificationBell />

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
                {/* Interactive Hearts Widget */}
                <button
                  onClick={() => setShowHeartModal(true)}
                  className="flex items-center gap-1 px-2.5 py-1 rounded-xl bg-[#182830] border border-[#ff4b4b]/30 text-[#ff4b4b] hover:scale-105 transition-transform cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#ff4b4b]"
                  title="Click to view Hearts & Regeneration Timer"
                >
                  <span>❤️</span>
                  <span>{stats.hearts}</span>
                </button>
                {/* Gems */}
                <div
                  className="hidden xl:flex items-center gap-1 px-2.5 py-1 rounded-xl bg-[#182830] border border-[#1cb0f6]/30 text-[#1cb0f6]"
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

      {/* Out of Hearts & Regeneration Modal */}
      {showHeartModal && stats && (
        <OutOfHeartsModal
          hearts={stats.hearts}
          maxHearts={stats.max_hearts || 5}
          secondsUntilNext={stats.heart_regeneration?.seconds_until_next}
          onClose={() => setShowHeartModal(false)}
          onRefreshStats={fetchStats}
        />
      )}
    </>
  );
};
