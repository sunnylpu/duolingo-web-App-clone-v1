"use client";

import React, { useState } from "react";
import { socialService } from "@/services/social-service";

interface FollowButtonProps {
  userId: string;
  initialIsFollowing: boolean;
  onToggle?: (newIsFollowing: boolean) => void;
  size?: "sm" | "md";
}

export const FollowButton: React.FC<FollowButtonProps> = ({
  userId,
  initialIsFollowing,
  onToggle,
  size = "md",
}) => {
  const [isFollowing, setIsFollowing] = useState<boolean>(initialIsFollowing);
  const [loading, setLoading] = useState<boolean>(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      if (isFollowing) {
        await socialService.unfollowUser(userId);
        setIsFollowing(false);
        if (onToggle) onToggle(false);
      } else {
        await socialService.followUser(userId);
        setIsFollowing(true);
        if (onToggle) onToggle(true);
      }
    } catch (err) {
      console.error("Failed to toggle follow status:", err);
    } finally {
      setLoading(false);
    }
  };

  const isSm = size === "sm";

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className={`rounded-xl font-black text-xs uppercase tracking-wider transition-all shadow-sm ${
        isSm ? "px-3 py-1.5" : "px-4 py-2"
      } ${
        isFollowing
          ? "bg-[#182830] text-gray-300 border-2 border-[#37464f] hover:border-[#ff4b4b] hover:text-[#ff4b4b]"
          : "bg-[#1cb0f6] text-black hover:bg-[#20bdff] shadow-[0_2px_0_#1899d6]"
      }`}
    >
      {loading ? "..." : isFollowing ? "FOLLOWING" : "+ FOLLOW"}
    </button>
  );
};
