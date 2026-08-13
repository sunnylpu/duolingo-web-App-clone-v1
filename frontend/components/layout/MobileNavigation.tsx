"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export const MobileNavigation: React.FC = () => {
  const pathname = usePathname();

  const navItems = [
    { label: "Home", href: "/", icon: "🏠" },
    { label: "Learn", href: "/learn", icon: "📖" },
    { label: "Profile", href: "/profile", icon: "👤" },
    { label: "Settings", href: "/settings", icon: "⚙️" },
  ];

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#131f24] border-t border-[#37464f] px-2 py-2 flex justify-around items-center">
      {navItems.map((item) => {
        const isActive = pathname === item.href;
        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-col items-center py-1 px-3 rounded-xl text-xs font-bold transition-colors ${
              isActive
                ? "text-[#1cb0f6] bg-[#182830]"
                : "text-gray-400 hover:text-white"
            }`}
          >
            <span className="text-base">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
};
