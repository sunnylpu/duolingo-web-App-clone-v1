"use client";

import React, { useState } from "react";
import { PathResponse, SkillPath, UserStats } from "@/types";
import { CourseHeader } from "./components/CourseHeader";
import { DailyGoal } from "./components/DailyGoal";
import { UnitSection } from "./components/UnitSection";
import { SkillPreview } from "./components/SkillPreview";

interface LearningPathProps {
  pathData: PathResponse;
  stats?: UserStats | null;
  onStartLesson?: (skillId: string) => void;
}

export const LearningPath: React.FC<LearningPathProps> = ({
  pathData,
  stats,
  onStartLesson,
}) => {
  const [selectedSkill, setSelectedSkill] = useState<SkillPath | null>(null);

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Course Banner Header */}
      <CourseHeader
        course={pathData.course}
        totalUnits={pathData.units.length}
      />

      {/* Daily XP Progress Widget */}
      {stats && <DailyGoal stats={stats} />}

      {/* Unit Sections Stack */}
      <div className="space-y-4">
        {pathData.units.map((unit) => (
          <UnitSection
            key={unit.id}
            unit={unit}
            onSelectSkill={(skill) => setSelectedSkill(skill)}
          />
        ))}
      </div>

      {/* Skill Modal Popover */}
      <SkillPreview
        skill={selectedSkill}
        onClose={() => setSelectedSkill(null)}
        onStartLesson={onStartLesson}
      />
    </div>
  );
};
