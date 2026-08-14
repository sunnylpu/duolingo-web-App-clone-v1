import uuid
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.modules.progress.models import (
    SkillProgressModel,
    LessonAttemptModel,
    ExerciseAttemptModel,
    DailyActivityModel,
)


class ProgressRepository:
    """Handles data persistence for the Progress domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_skill_progress(self, user_id: str, skill_id: str) -> Optional[SkillProgressModel]:
        return (
            self.db.query(SkillProgressModel)
            .filter(
                SkillProgressModel.user_id == user_id,
                SkillProgressModel.skill_id == skill_id,
            )
            .first()
        )

    def get_user_skill_progresses(self, user_id: str) -> List[SkillProgressModel]:
        return self.db.query(SkillProgressModel).filter(SkillProgressModel.user_id == user_id).all()

    def upsert_skill_progress(
        self,
        progress_id: str,
        user_id: str,
        skill_id: str,
        status: str = "locked",
        completion_percent: float = 0.0,
        crown_level: int = 0,
        lessons_completed: int = 0,
        xp_earned: int = 0,
        commit: bool = True,
    ) -> SkillProgressModel:
        record = self.get_skill_progress(user_id, skill_id)
        if not record:
            record = SkillProgressModel(
                id=progress_id,
                user_id=user_id,
                skill_id=skill_id,
                status=status,
                completion_percent=completion_percent,
                crown_level=crown_level,
                lessons_completed=lessons_completed,
                xp_earned=xp_earned,
            )
            self.db.add(record)
        else:
            record.status = status
            record.completion_percent = completion_percent
            record.crown_level = crown_level
            record.lessons_completed = lessons_completed
            record.xp_earned = xp_earned

        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(record)
        return record

    def record_daily_activity(
        self,
        activity_id: str,
        user_id: str,
        activity_date: date,
        xp_earned: int = 0,
        lessons_completed: int = 0,
        minutes_learned: int = 0,
        goal_completed: bool = False,
        commit: bool = True,
    ) -> DailyActivityModel:
        act = (
            self.db.query(DailyActivityModel)
            .filter(
                (DailyActivityModel.id == activity_id)
                | (
                    (DailyActivityModel.user_id == user_id)
                    & (DailyActivityModel.activity_date == activity_date)
                )
            )
            .first()
        )
        if not act:
            act = DailyActivityModel(
                id=activity_id,
                user_id=user_id,
                activity_date=activity_date,
                xp_earned=xp_earned,
                lessons_completed=lessons_completed,
                minutes_learned=minutes_learned,
                goal_completed=goal_completed,
            )
            self.db.add(act)
        else:
            act.xp_earned += xp_earned
            act.lessons_completed += lessons_completed
            act.minutes_learned += minutes_learned
            act.goal_completed = goal_completed or act.goal_completed

        self.db.flush()
        if commit:
            self.db.commit()
            self.db.refresh(act)
        return act
