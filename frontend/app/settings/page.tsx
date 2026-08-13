import React from "react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export default function SettingsPage() {
  const sections = [
    { title: "Profile Preferences", desc: "Manage display name, avatar, and public profile visibility." },
    { title: "Notifications & Reminders", desc: "Configure daily study reminders and streak notifications." },
    { title: "Appearance & Accessibility", desc: "Toggle dark mode, sound effects, and font sizing." },
  ];

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div>
        <h1 className="text-2xl md:text-3xl font-extrabold text-white">
          Settings
        </h1>
        <p className="text-sm text-gray-400 mt-1">
          Preferences & Application Configuration
        </p>
      </div>

      <div className="space-y-4">
        {sections.map((sec) => (
          <Card key={sec.title} className="flex justify-between items-center p-5">
            <div>
              <h3 className="font-bold text-base text-white">{sec.title}</h3>
              <p className="text-xs text-gray-400 mt-0.5">{sec.desc}</p>
            </div>
            <Badge variant="yellow">Coming Soon</Badge>
          </Card>
        ))}
      </div>
    </div>
  );
}
