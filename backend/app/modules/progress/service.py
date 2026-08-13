from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.models import SkillProgressModel, LessonAttemptModel
from app.modules.course.models import CourseModel, UnitModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.progress.schemas import ProgressResponse, SkillProgressSummary
from app.modules.course.schemas import (
    PathResponse,
    CourseSummaryResponse,
    UnitPathResponse,
    SkillPathResponse,
)
from app.modules.user.models import UserModel
from app.shared.errors import NotFoundError


class ProgressService:
    """Central Progression Domain Engine & Single Source of Truth for Skill Access and Path Status."""

    def __init__(self, db_or_repo: Any):
        if isinstance(db_or_repo, Session):
            self.db = db_or_repo
            self.repository = ProgressRepository(db_or_repo)
        elif hasattr(db_or_repo, "db"):
            self.repository = db_or_repo
            self.db = db_or_repo.db
        else:
            raise ValueError("ProgressService requires a Session or ProgressRepository instance.")

    def evaluate_skill_state(self, user_id: str, skill: SkillModel) -> Dict[str, Any]:
        """
        Dynamically calculates and returns skill status, completion percent, crown level,
        and prerequisite metadata based on authoritative completed lessons and seeded progress.
        """
        all_skills = {s.id: s for s in self.db.query(SkillModel).all()}
        prereq_title = None
        if skill.prerequisite_skill_id and skill.prerequisite_skill_id in all_skills:
            prereq_title = all_skills[skill.prerequisite_skill_id].title

        # Check existing SkillProgressModel record (for seeded states)
        user_prog = self.repository.get_skill_progress(user_id, skill.id)

        # Query all lessons for this skill
        lessons = self.db.query(LessonModel).filter(LessonModel.skill_id == skill.id).all()
        lesson_ids = [l.id for l in lessons]
        total_lessons = max(1, len(lessons))

        # Query completed lesson attempts for this skill and user
        completed_attempts = []
        if lesson_ids:
            completed_attempts = (
                self.db.query(LessonAttemptModel)
                .filter(
                    LessonAttemptModel.user_id == user_id,
                    LessonAttemptModel.lesson_id.in_(lesson_ids),
                    LessonAttemptModel.status == "completed",
                )
                .all()
            )

        unique_completed_lessons = {a.lesson_id for a in completed_attempts}
        completed_count = len(unique_completed_lessons)

        if completed_count > 0:
            completion_percent = float(min(100.0, (completed_count / total_lessons) * 100.0))
            crown_level = min(5, completed_count)
        elif user_prog:
            completion_percent = user_prog.completion_percent
            crown_level = user_prog.crown_level
        else:
            completion_percent = 0.0
            crown_level = 0

        # Check prerequisite status if prerequisite_skill_id is set
        prereq_completed = True
        if skill.prerequisite_skill_id:
            prereq_skill = all_skills.get(skill.prerequisite_skill_id)
            if prereq_skill:
                prereq_eval = self.evaluate_skill_state(user_id, prereq_skill)
                prereq_completed = (prereq_eval["status"] == "completed")

        # Determine Status
        if completion_percent >= 100.0 or (user_prog and user_prog.status == "completed"):
            status = "completed"
            completion_percent = 100.0
        elif completion_percent > 0 or (user_prog and user_prog.status == "in_progress"):
            status = "in_progress"
        elif not skill.prerequisite_skill_id or prereq_completed:
            status = "available"
        else:
            status = "locked"

        return {
            "skill_id": skill.id,
            "title": skill.title,
            "status": status,
            "completion_percent": completion_percent,
            "crown_level": crown_level,
            "lessons_completed": completed_count,
            "total_lessons": total_lessons,
            "xp_earned": completed_count * skill.xp_reward,
            "prerequisite_skill_id": skill.prerequisite_skill_id,
            "prerequisite_title": prereq_title,
        }

    def get_skill_status(self, user_id: str, skill_id: str) -> Dict[str, Any]:
        skill = self.db.query(SkillModel).filter(SkillModel.id == skill_id).first()
        if not skill:
            raise NotFoundError(f"Skill '{skill_id}' not found.")
        return self.evaluate_skill_state(user_id, skill)

    def get_learning_path(
        self, current_user: UserModel, course_id: Optional[str] = None
    ) -> PathResponse:
        course = None
        if course_id:
            course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()

        if not course:
            course = self.db.query(CourseModel).filter(CourseModel.is_active == True).first()

        if not course:
            raise NotFoundError("No active courses found for learning path.")

        units = (
            self.db.query(UnitModel)
            .filter(UnitModel.course_id == course.id)
            .order_by(UnitModel.order_index)
            .all()
        )

        unit_paths: List[UnitPathResponse] = []
        recommended_skill_id: Optional[str] = None
        first_available_skill_id: Optional[str] = None

        for u in units:
            skills = (
                self.db.query(SkillModel)
                .filter(SkillModel.unit_id == u.id)
                .order_by(SkillModel.order_index)
                .all()
            )

            skill_paths: List[SkillPathResponse] = []
            for s in skills:
                state = self.evaluate_skill_state(current_user.id, s)

                if state["status"] == "in_progress" and not recommended_skill_id:
                    recommended_skill_id = s.id
                elif state["status"] == "available" and not first_available_skill_id:
                    first_available_skill_id = s.id

                sp_id = f"sp_{current_user.id}_{s.id}"
                self.repository.upsert_skill_progress(
                    progress_id=sp_id,
                    user_id=current_user.id,
                    skill_id=s.id,
                    status=state["status"],
                    completion_percent=state["completion_percent"],
                    crown_level=state["crown_level"],
                    lessons_completed=state["lessons_completed"],
                    xp_earned=state["xp_earned"],
                    commit=True,
                )

                skill_paths.append(
                    SkillPathResponse(
                        id=s.id,
                        title=s.title,
                        description=s.description,
                        order_index=s.order_index,
                        xp_reward=s.xp_reward,
                        prerequisite_skill_id=s.prerequisite_skill_id,
                        prerequisite_title=state["prerequisite_title"],
                        status=state["status"],
                        completion_percent=state["completion_percent"],
                        crown_level=state["crown_level"],
                    )
                )

            unit_paths.append(
                UnitPathResponse(
                    id=u.id,
                    title=u.title,
                    description=u.description,
                    order_index=u.order_index,
                    skills=skill_paths,
                )
            )

        final_recommended = recommended_skill_id or first_available_skill_id

        return PathResponse(
            course=CourseSummaryResponse.model_validate(course),
            recommended_skill_id=final_recommended,
            units=unit_paths,
        )

    def get_user_progress_summary(self, current_user: UserModel) -> ProgressResponse:
        skills = self.db.query(SkillModel).all()
        summaries: List[SkillProgressSummary] = []

        for s in skills:
            state = self.evaluate_skill_state(current_user.id, s)
            summaries.append(
                SkillProgressSummary(
                    skill_id=s.id,
                    status=state["status"],
                    completion_percent=state["completion_percent"],
                    crown_level=state["crown_level"],
                    lessons_completed=state["lessons_completed"],
                    xp_earned=state["xp_earned"],
                    prerequisite_skill_id=s.prerequisite_skill_id,
                    prerequisite_title=state["prerequisite_title"],
                )
            )
        return ProgressResponse(skills=summaries)
