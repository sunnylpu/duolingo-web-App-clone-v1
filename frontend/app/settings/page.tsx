"use client";

import React from "react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { NotificationPreferences } from "@/features/notifications";

export default function SettingsPage() {
  const sections = [
    { title: "Profile Preferences", desc: "Manage display name, avatar, and public profile visibility." },
    { title: "Appearance & Accessibility", desc: "Toggle dark mode, sound effects, and font sizing." },
  ];

  return (
    <div className="space-y-6 max-w-3xl mx-auto py-4">
      <div>
        <h1 className="text-2xl md:text-3xl font-extrabold text-white">
          Settings
        </h1>
        <p className="text-sm text-gray-400 mt-1">
          Preferences & Application Configuration
        </p>
      </div>

      {/* Functional Notification Preferences Section */}
      <NotificationPreferences />

      {/* Other Settings Sections (Placeholders) */}
      <div className="space-y-4 pt-2">
        <h3 className="text-sm font-black text-gray-400 uppercase tracking-wider">
          Other Settings
        </h3>
        {sections.map((sec) => (
          <Card key={sec.title} className="flex justify-between items-center p-5 bg-[#182830] border-2 border-[#37464f]">
            <div>
              <h4 className="font-bold text-sm text-white">{sec.title}</h4>
              <p className="text-xs text-gray-400 mt-0.5">{sec.desc}</p>
            </div>
            <Badge variant="yellow">Coming Soon</Badge>
          </Card>
        ))}
      </div>
    </div>
  );
}
