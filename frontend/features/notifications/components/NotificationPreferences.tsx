"use client";

import React, { useState, useEffect } from "react";
import {
  notificationService,
  NotificationPreferences as NotificationPreferencesType,
} from "@/services/notification-service";
import { Card } from "@/components/ui/Card";

export const NotificationPreferences: React.FC = () => {
  const [prefs, setPrefs] = useState<NotificationPreferencesType | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    notificationService
      .getPreferences()
      .then(setPrefs)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const handleToggle = async (key: keyof Omit<NotificationPreferencesType, "user_id">) => {
    if (!prefs) return;
    const newVal = !prefs[key];
    setPrefs({ ...prefs, [key]: newVal });
    setSaving(true);
    setMessage(null);

    try {
      await notificationService.updatePreferences({ [key]: newVal });
      setMessage("Preferences updated.");
    } catch (err) {
      console.error("Failed to save preference", err);
      // Revert on failure
      setPrefs({ ...prefs, [key]: !newVal });
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-4 animate-pulse">
        <div className="h-6 w-48 bg-[#131f24] rounded" />
        <div className="space-y-3">
          <div className="h-10 bg-[#131f24] rounded-xl" />
          <div className="h-10 bg-[#131f24] rounded-xl" />
        </div>
      </Card>
    );
  }

  if (!prefs) return null;

  const CATEGORIES = [
    { key: "daily_reminders", label: "Daily Reminders", desc: "Reminders to practice language lessons daily" },
    { key: "streak_reminders", label: "Streak Reminders", desc: "Alerts when your active streak is at risk" },
    { key: "quest_reminders", label: "Quest Reminders", desc: "Notifications when daily quests are incomplete" },
    { key: "achievement_notifications", label: "Achievement & Progress", desc: "Celebration alerts for badges, units, and courses" },
    { key: "social_notifications", label: "Social Activity", desc: "Updates from friends you follow" },
  ] as const;

  return (
    <Card className="p-6 bg-[#182830] border-2 border-[#37464f] space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-black text-white uppercase tracking-wider flex items-center gap-2">
            <span>🔔</span>
            <span>Notification Preferences</span>
          </h3>
          <p className="text-xs text-gray-400 font-medium mt-0.5">
            Configure which reminder and celebration notifications you receive
          </p>
        </div>
        {message && (
          <span className="text-xs font-black text-[#58cc02] bg-[#58cc02]/10 px-3 py-1 rounded-lg border border-[#58cc02]/30">
            {message}
          </span>
        )}
      </div>

      <div className="space-y-4 divide-y divide-[#37464f]/50">
        {CATEGORIES.map(({ key, label, desc }) => (
          <div key={key} className="pt-3 first:pt-0 flex items-center justify-between gap-4">
            <div>
              <h4 className="text-xs font-black text-white">{label}</h4>
              <p className="text-[11px] text-gray-400 font-medium mt-0.5">{desc}</p>
            </div>

            <button
              type="button"
              onClick={() => handleToggle(key)}
              disabled={saving}
              className={`w-12 h-6 rounded-full transition-colors relative border-2 ${
                prefs[key]
                  ? "bg-[#58cc02] border-[#58cc02]"
                  : "bg-[#131f24] border-[#37464f]"
              }`}
            >
              <span
                className={`w-4 h-4 rounded-full bg-white absolute top-0.5 transition-all ${
                  prefs[key] ? "right-1" : "left-1"
                }`}
              />
            </button>
          </div>
        ))}
      </div>
    </Card>
  );
};
