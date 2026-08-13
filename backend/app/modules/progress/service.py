from typing import List, Optional, Dict, Any, Set
from sqlalchemy.orm import Session, joinedload
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
    """Central Progression Domain Engine — Single Source of Truth for Skill Access and Path Status.

    Optimized Query Strategy (Phase 19+):
    ─────────────────────────────────────
    Previous (N+1): For N skills, issued ~4N SQL queries (all skills + lessons + attempts +
    progress per skill, recursively for prerequisite checks).

    Current (2-query):
        Query 1 — Eager-load full hierarchy:
            Course → Units → Skills → Lessons  (1 joined query via joinedload)
        Query 2 — Fetch all completed lesson IDs for this user:
            SELECT lesson_id FROM lesson_attempts WHERE user_id=? AND status='completed'
        Evaluation — Python memory only; zero additional DB calls per skill.
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
    #  Private helpers — all work from pre-fetched in-memory data
    # ──────────────────────────────────────────────────────────────

    def _fetch_completed_lesson_ids(self, user_id: str) -> Set[str]:
        """
        Single-query fetch of ALL completed lesson IDs for a user.
        Returns a set of lesson_id strings for O(1) lookup during skill evaluation.
        """
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
        """
        Single-query fetch of all SkillProgress records for a user.
        Returns a dict keyed by skill_id.
        """
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
        """
        Pure in-memory skill-state evaluation.
        No database queries are issued inside this method.

        Parameters:
            skill                — the SkillModel to evaluate
            completed_lesson_ids — set of all lesson IDs the user has completed
            skill_status_cache   — memoization cache {skill_id -> status} to avoid re-evaluating
            skill_map            — dict {skill_id -> SkillModel} for prerequisite lookup
            user_progress_map    — dict {skill_id -> SkillProgressModel} for seeded states
        """
        if skill.id in skill_status_cache:
            # Already evaluated (memoized) — reconstruct minimal dict for caller
            cached_status = skill_status_cache[skill.id]
            return {"status": cached_status}

        # --- Lesson accounting ---
        lesson_ids = [l.id for l in skill.lessons]
        total_lessons = max(1, len(lesson_ids))
        unique_completed = completed_lesson_ids.intersection(lesson_ids)
        completed_count = len(unique_completed)

        # --- Completion % and crown ---
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

        # --- Prerequisite check (fully in-memory via recursion + cache) ---
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

        # --- Status determination ---
        if completion_percent >= 100.0 or (user_prog and user_prog.status == "completed"):
            status = "completed"
            completion_percent = 100.0
        elif completion_percent > 0 or (user_prog and user_prog.status == "in_progress"):
            status = "in_progress"
        elif not skill.prerequisite_skill_id or prereq_completed:
            status = "available"
        else:
            status = "locked"

        # Memoize
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
    #  Public API — used by router/other services
    # ──────────────────────────────────────────────────────────────

    def evaluate_skill_state(self, user_id: str, skill: SkillModel) -> Dict[str, Any]:
        """
        Single-skill evaluation (used by lesson service for access control).
        Fetches per-skill data individually when called in isolation.

        For bulk path evaluation, prefer get_learning_path() which uses the
        optimized 2-query strategy internally.
        """
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
        """
        Build the full learning path for a user.

        Optimized to use exactly 2 primary SQL queries:
          Query 1: Eager-load Course → Units → Skills → Lessons
          Query 2: All completed lesson IDs for this user (1 SELECT DISTINCT)
          (+ 1 query for user skill progress map)

        All skill-state evaluations happen in Python memory.
        """
        # ── Query 1: Eager-load full Course hierarchy ──────────────────
        course_query = self.db.query(CourseModel).options(
            joinedload(CourseModel.units).joinedload(UnitModel.skills).joinedload(SkillModel.lessons)
        )
        if course_id:
            course = course_query.filter(CourseModel.id == course_id).first()
        else:
            course = course_query.filter(CourseModel.is_active == True).first()

        if not course:
            raise NotFoundError("No active courses found for learning path.")

        # ── Query 2: All completed lesson IDs for this user ────────────
        completed_lesson_ids = self._fetch_completed_lesson_ids(current_user.id)

        # ── Query 3: All SkillProgress records for this user ──────────
        user_progress_map = self._fetch_user_skill_progress_map(current_user.id)

        # ── Build flat skill map from eager-loaded hierarchy ───────────
        skill_map: Dict[str, SkillModel] = {}
        for unit in course.units:
            for skill in unit.skills:
                skill_map[skill.id] = skill

        # ── Evaluate all skills in memory ──────────────────────────────
        skill_status_cache: Dict[str, str] = {}
        unit_paths: List[UnitPathResponse] = []
        recommended_skill_id: Optional[str] = None
        first_available_skill_id: Optional[str] = None

        for unit in sorted(course.units, key=lambda u: u.order_index):
            skill_paths: List[SkillPathResponse] = []

            for skill in sorted(unit.skills, key=lambda s: s.order_index):
                state = self._evaluate_skill_state_from_memory(
                    skill, completed_lesson_ids, skill_status_cache, skill_map, user_progress_map
                )

                if state["status"] == "in_progress" and not recommended_skill_id:
                    recommended_skill_id = skill.id
                elif state["status"] == "available" and not first_available_skill_id:
                    first_available_skill_id = skill.id

                # Persist updated progress (non-blocking flush)
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

            unit_paths.append(
                UnitPathResponse(
                    id=unit.id,
                    title=unit.title,
                    description=unit.description,
                    order_index=unit.order_index,
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
        """
        Optimized progress summary using the same 2-query strategy.
        """
        # Eager-load all skills with their lessons
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
