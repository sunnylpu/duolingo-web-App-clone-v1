from typing import List, Optional, Dict, Any, Set
from sqlalchemy.orm import Session, joinedload
from app.modules.progress.repository import ProgressRepository
from app.modules.progress.models import (
    SkillProgressModel,
    LessonAttemptModel,
    UnitMilestoneModel,
    CourseMilestoneModel,
)
from app.modules.course.models import CourseModel, UnitModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.progress.schemas import ProgressResponse, SkillProgressSummary
from app.modules.course.schemas import (
    PathResponse,
    CourseSummaryResponse,
    UnitPathResponse,
    SkillPathResponse,
    UnitProgressSummaryResponse,
    CourseProgressSummaryResponse,
)
from app.modules.user.models import UserModel
from app.shared.errors import NotFoundError

UNIT_COMPLETION_XP = 50
COURSE_COMPLETION_XP = 500

COURSE_MASTER_ACHIEVEMENTS = {
    "crs_english": "ENGLISH_MASTER",
    "crs_spanish": "SPANISH_MASTER",
    "crs_french": "FRENCH_MASTER",
}


class ProgressService:
    """Central Progression Domain Engine — Single Source of Truth for Skill, Unit, and Course Status.

    Optimized Query Strategy (Phase 19+):
    ─────────────────────────────────────
    Query 1 — Eager-load full hierarchy:
        Course → Units → Skills → Lessons  (1 joined query via joinedload)
    Query 2 — Fetch all completed lesson IDs for this user:
        SELECT lesson_id FROM lesson_attempts WHERE user_id=? AND status='completed'
    Evaluation — Python memory only; zero additional DB calls per skill, unit, or course.
    """

    def __init__(self, db_or_repo: Any):
        if isinstance(db_or_repo, Session):
            self.db = db_or_repo
            self.repository = ProgressRepository(db_or_repo)
        elif hasattr(db_or_repo, "db"):
            self.repository = db_or_repo
            self.db = db_or_repo.db
        else:
            raise ValueError("ProgressService requires a Session or ProgressRepository instance.")

    # ──────────────────────────────────────────────────────────────
    #  Private helpers — in-memory execution
    # ──────────────────────────────────────────────────────────────

    def _fetch_completed_lesson_ids(self, user_id: str) -> Set[str]:
        rows = (
            self.db.query(LessonAttemptModel.lesson_id)
            .filter(
                LessonAttemptModel.user_id == user_id,
                LessonAttemptModel.status == "completed",
            )
            .distinct()
            .all()
        )
        return {row.lesson_id for row in rows}

    def _fetch_user_skill_progress_map(self, user_id: str) -> Dict[str, SkillProgressModel]:
        records = (
            self.db.query(SkillProgressModel)
            .filter(SkillProgressModel.user_id == user_id)
            .all()
        )
        return {r.skill_id: r for r in records}

    def _evaluate_skill_state_from_memory(
        self,
        skill: SkillModel,
        completed_lesson_ids: Set[str],
        skill_status_cache: Dict[str, str],
        skill_map: Dict[str, SkillModel],
        user_progress_map: Dict[str, SkillProgressModel],
    ) -> Dict[str, Any]:
        if skill.id in skill_status_cache:
            cached_status = skill_status_cache[skill.id]
            return {"status": cached_status}

        lesson_ids = [l.id for l in skill.lessons]
        total_lessons = max(1, len(lesson_ids))
        unique_completed = completed_lesson_ids.intersection(lesson_ids)
        completed_count = len(unique_completed)

        user_prog = user_progress_map.get(skill.id)
        if completed_count > 0:
            completion_percent = float(min(100.0, (completed_count / total_lessons) * 100.0))
            crown_level = min(5, completed_count)
        elif user_prog:
            completion_percent = user_prog.completion_percent
            crown_level = user_prog.crown_level
        else:
            completion_percent = 0.0
            crown_level = 0

        prereq_completed = True
        prereq_title = None
        if skill.prerequisite_skill_id:
            prereq_skill = skill_map.get(skill.prerequisite_skill_id)
            if prereq_skill:
                prereq_title = prereq_skill.title
                prereq_eval = self._evaluate_skill_state_from_memory(
                    prereq_skill, completed_lesson_ids, skill_status_cache, skill_map, user_progress_map
                )
                prereq_completed = prereq_eval["status"] == "completed"

        if completion_percent >= 100.0 or (user_prog and user_prog.status == "completed"):
            status = "completed"
            completion_percent = 100.0
        elif completion_percent > 0 or (user_prog and user_prog.status == "in_progress"):
            status = "in_progress"
        elif not skill.prerequisite_skill_id or prereq_completed:
            status = "available"
        else:
            status = "locked"

        skill_status_cache[skill.id] = status

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

    # ──────────────────────────────────────────────────────────────
    #  Public API — Milestones, Path & Course Summaries
    # ──────────────────────────────────────────────────────────────

    def check_and_grant_unit_milestone(self, user_id: str, unit_id: str) -> Dict[str, Any]:
        existing = (
            self.db.query(UnitMilestoneModel)
            .filter(
                UnitMilestoneModel.user_id == user_id,
                UnitMilestoneModel.unit_id == unit_id,
            )
            .first()
        )
        if existing:
            return {"unit_bonus_xp": 0, "unit_completed": False, "already_awarded": True}

        milestone_id = f"um_{user_id}_{unit_id}"
        milestone = UnitMilestoneModel(
            id=milestone_id,
            user_id=user_id,
            unit_id=unit_id,
            reward_xp=UNIT_COMPLETION_XP,
        )
        self.db.add(milestone)

        from app.modules.gamification.repository import GamificationRepository
        gamification_repo = GamificationRepository(self.db)
        stats = gamification_repo.get_user_stats(user_id)
        if stats:
            stats.total_xp += UNIT_COMPLETION_XP
            stats.daily_xp += UNIT_COMPLETION_XP

        self.db.flush()

        return {
            "unit_bonus_xp": UNIT_COMPLETION_XP,
            "unit_completed": True,
            "already_awarded": False,
        }

    def check_and_grant_course_milestone(self, user_id: str, course_id: str) -> Dict[str, Any]:
        """
        Durable top-level course milestone reward check (+500 XP).
        Guarantees idempotent award and evaluates course mastery achievement.
        """
        existing = (
            self.db.query(CourseMilestoneModel)
            .filter(
                CourseMilestoneModel.user_id == user_id,
                CourseMilestoneModel.course_id == course_id,
            )
            .first()
        )
        if existing:
            return {"course_bonus_xp": 0, "course_completed": False, "already_awarded": True}

        milestone_id = f"cm_{user_id}_{course_id}"
        milestone = CourseMilestoneModel(
            id=milestone_id,
            user_id=user_id,
            course_id=course_id,
            reward_xp=COURSE_COMPLETION_XP,
        )
        self.db.add(milestone)

        from app.modules.gamification.repository import GamificationRepository
        gamification_repo = GamificationRepository(self.db)
        stats = gamification_repo.get_user_stats(user_id)
        if stats:
            stats.total_xp += COURSE_COMPLETION_XP
            stats.daily_xp += COURSE_COMPLETION_XP

        # Check and grant course master achievement if code mapped
        ach_code = COURSE_MASTER_ACHIEVEMENTS.get(course_id)
        if ach_code:
            ach = gamification_repo.get_achievement_by_code(ach_code)
            if ach:
                gamification_repo.grant_user_achievement(
                    user_achievement_id=f"uach_{user_id}_{ach.id}",
                    user_id=user_id,
                    achievement_id=ach.id,
                )

        self.db.flush()

        return {
            "course_bonus_xp": COURSE_COMPLETION_XP,
            "course_completed": True,
            "already_awarded": False,
        }

    def evaluate_skill_state(self, user_id: str, skill: SkillModel) -> Dict[str, Any]:
        all_skills = {s.id: s for s in self.db.query(SkillModel).options(
            joinedload(SkillModel.lessons)
        ).all()}
        completed_lesson_ids = self._fetch_completed_lesson_ids(user_id)
        user_progress_map = self._fetch_user_skill_progress_map(user_id)
        cache: Dict[str, str] = {}
        return self._evaluate_skill_state_from_memory(
            skill, completed_lesson_ids, cache, all_skills, user_progress_map
        )

    def get_skill_status(self, user_id: str, skill_id: str) -> Dict[str, Any]:
        skill = (
            self.db.query(SkillModel)
            .options(joinedload(SkillModel.lessons))
            .filter(SkillModel.id == skill_id)
            .first()
        )
        if not skill:
            raise NotFoundError(f"Skill '{skill_id}' not found.")
        return self.evaluate_skill_state(user_id, skill)

    def get_learning_path(
        self, current_user: UserModel, course_id: Optional[str] = None
    ) -> PathResponse:
        course_query = self.db.query(CourseModel).options(
            joinedload(CourseModel.units).joinedload(UnitModel.skills).joinedload(SkillModel.lessons)
        )
        if course_id:
            course = course_query.filter(CourseModel.id == course_id).first()
        else:
            course = course_query.filter(CourseModel.id == "crs_english", CourseModel.is_active == True).first()
            if not course:
                course = course_query.filter(CourseModel.is_active == True).first()

        if not course:
            raise NotFoundError("No active courses found for learning path.")

        completed_lesson_ids = self._fetch_completed_lesson_ids(current_user.id)
        user_progress_map = self._fetch_user_skill_progress_map(current_user.id)

        skill_map: Dict[str, SkillModel] = {}
        for unit in course.units:
            for skill in unit.skills:
                skill_map[skill.id] = skill

        skill_status_cache: Dict[str, str] = {}
        unit_paths: List[UnitPathResponse] = []
        recommended_skill_id: Optional[str] = None
        first_available_skill_id: Optional[str] = None
        prev_unit_completed = True

        sorted_units = sorted(course.units, key=lambda u: u.order_index)
        total_units_count = len(sorted_units)
        completed_units_count = 0
        total_course_skills = 0
        completed_course_skills = 0
        total_course_lessons = 0
        completed_course_lessons = 0

        for idx, unit in enumerate(sorted_units):
            skill_paths: List[SkillPathResponse] = []

            for skill in sorted(unit.skills, key=lambda s: s.order_index):
                state = self._evaluate_skill_state_from_memory(
                    skill, completed_lesson_ids, skill_status_cache, skill_map, user_progress_map
                )

                if state["status"] == "in_progress" and not recommended_skill_id:
                    recommended_skill_id = skill.id
                elif state["status"] == "available" and not first_available_skill_id:
                    first_available_skill_id = skill.id

                total_course_lessons += state["total_lessons"]
                completed_course_lessons += state["lessons_completed"]

                sp_id = f"sp_{current_user.id}_{skill.id}"
                self.repository.upsert_skill_progress(
                    progress_id=sp_id,
                    user_id=current_user.id,
                    skill_id=skill.id,
                    status=state["status"],
                    completion_percent=state["completion_percent"],
                    crown_level=state["crown_level"],
                    lessons_completed=state["lessons_completed"],
                    xp_earned=state["xp_earned"],
                    commit=True,
                )

                skill_paths.append(
                    SkillPathResponse(
                        id=skill.id,
                        title=skill.title,
                        description=skill.description,
                        order_index=skill.order_index,
                        xp_reward=skill.xp_reward,
                        prerequisite_skill_id=skill.prerequisite_skill_id,
                        prerequisite_title=state.get("prerequisite_title"),
                        status=state["status"],
                        completion_percent=state["completion_percent"],
                        crown_level=state["crown_level"],
                    )
                )

            u_total_skills = len(skill_paths)
            u_completed_skills = sum(1 for s in skill_paths if s.status == "completed")
            total_course_skills += u_total_skills
            completed_course_skills += u_completed_skills

            u_completion_percent = (
                round((u_completed_skills / u_total_skills) * 100.0, 1) if u_total_skills > 0 else 0.0
            )

            if u_completed_skills == u_total_skills and u_total_skills > 0:
                unit_status = "completed"
                completed_units_count += 1
            elif u_completed_skills > 0 or any(s.status in ("in_progress", "completed") for s in skill_paths):
                unit_status = "in_progress"
            elif idx == 0 or prev_unit_completed or any(s.status == "available" for s in skill_paths):
                unit_status = "available"
            else:
                unit_status = "locked"

            prev_unit_completed = (unit_status == "completed")

            unit_paths.append(
                UnitPathResponse(
                    id=unit.id,
                    title=unit.title,
                    description=unit.description,
                    order_index=unit.order_index,
                    status=unit_status,
                    completion_percent=u_completion_percent,
                    completed_skills=u_completed_skills,
                    total_skills=u_total_skills,
                    skills=skill_paths,
                )
            )

        final_recommended = recommended_skill_id or first_available_skill_id
        recommended_unit_id: Optional[str] = None
        recommended_lesson_id: Optional[str] = None

        if final_recommended and final_recommended in skill_map:
            rec_skill = skill_map[final_recommended]
            recommended_unit_id = rec_skill.unit_id
            rec_lessons = sorted(rec_skill.lessons, key=lambda l: l.order_index)
            for lsn in rec_lessons:
                if lsn.id not in completed_lesson_ids:
                    recommended_lesson_id = lsn.id
                    break
            if not recommended_lesson_id and rec_lessons:
                recommended_lesson_id = rec_lessons[0].id

        course_progress_pct = (
            round((completed_course_skills / total_course_skills) * 100.0, 1)
            if total_course_skills > 0
            else 0.0
        )

        course_status = (
            "completed"
            if completed_units_count == total_units_count and total_units_count > 0
            else "in_progress"
            if completed_units_count > 0 or completed_course_skills > 0
            else "available"
        )

        course_summary = CourseSummaryResponse(
            id=course.id,
            name=course.name,
            code=course.code,
            source_language=course.source_language,
            target_language=course.target_language,
            description=course.description,
            is_active=course.is_active,
            status=course_status,
            total_units=total_units_count,
            completed_units=completed_units_count,
            total_skills=total_course_skills,
            completed_skills=completed_course_skills,
            total_lessons=total_course_lessons,
            completed_lessons=completed_course_lessons,
            progress_percent=course_progress_pct,
        )

        return PathResponse(
            course=course_summary,
            recommended_skill_id=final_recommended,
            recommended_lesson_id=recommended_lesson_id,
            recommended_unit_id=recommended_unit_id,
            units=unit_paths,
        )

    def get_user_course_progress(
        self, current_user: UserModel, course_id: str
    ) -> CourseProgressSummaryResponse:
        """
        Lightweight API endpoint returning course-level progression summary for a user.
        """
        path = self.get_learning_path(current_user=current_user, course_id=course_id)
        c = path.course
        return CourseProgressSummaryResponse(
            course_id=c.id,
            course_name=c.name,
            status=c.status,
            completion_percent=c.progress_percent,
            completed_units=c.completed_units,
            total_units=c.total_units,
            completed_skills=c.completed_skills,
            total_skills=c.total_skills,
            completed_lessons=c.completed_lessons,
            total_lessons=c.total_lessons,
        )

    def get_user_unit_progress(
        self, current_user: UserModel, course_id: Optional[str] = None
    ) -> List[UnitProgressSummaryResponse]:
        path = self.get_learning_path(current_user=current_user, course_id=course_id)
        results = []
        for u in path.units:
            results.append(
                UnitProgressSummaryResponse(
                    unit_id=u.id,
                    title=u.title,
                    status=u.status,
                    completion_percent=u.completion_percent,
                    completed_skills=u.completed_skills,
                    total_skills=u.total_skills,
                )
            )
        return results

    def get_user_progress_summary(self, current_user: UserModel) -> ProgressResponse:
        all_skills = (
            self.db.query(SkillModel)
            .options(joinedload(SkillModel.lessons))
            .all()
        )
        skill_map = {s.id: s for s in all_skills}
        completed_lesson_ids = self._fetch_completed_lesson_ids(current_user.id)
        user_progress_map = self._fetch_user_skill_progress_map(current_user.id)
        cache: Dict[str, str] = {}

        summaries: List[SkillProgressSummary] = []
        for skill in all_skills:
            state = self._evaluate_skill_state_from_memory(
                skill, completed_lesson_ids, cache, skill_map, user_progress_map
            )
            summaries.append(
                SkillProgressSummary(
                    skill_id=skill.id,
                    status=state["status"],
                    completion_percent=state["completion_percent"],
                    crown_level=state["crown_level"],
                    lessons_completed=state["lessons_completed"],
                    xp_earned=state["xp_earned"],
                    prerequisite_skill_id=skill.prerequisite_skill_id,
                    prerequisite_title=state.get("prerequisite_title"),
                )
            )
        return ProgressResponse(skills=summaries)
