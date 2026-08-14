from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from app.modules.course.models import CourseModel, UnitModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.user.models import UserModel
from app.modules.progress.service import ProgressService
from app.modules.search.schemas import SearchResponse, SearchResultItem


class SearchService:
    """
    Search domain service performing normalized multi-entity curriculum search
    with deterministic relevance ranking.
    """

    def __init__(self, db: Session):
        self.db = db
        self.progress_service = ProgressService(db)

    def search_curriculum(
        self,
        query: str,
        current_user: UserModel,
        course_id: Optional[str] = None,
        item_type: Optional[str] = None,
        limit: int = 20,
    ) -> SearchResponse:
        clean_q = query.strip().lower()
        if not clean_q:
            return SearchResponse(query=query, total_results=0, results=[])

        raw_results: List[Dict[str, Any]] = []

        # 1. Search Courses
        if not item_type or item_type.lower() == "course":
            courses = self.db.query(CourseModel).filter(CourseModel.is_active == True).all()
            for c in courses:
                score = self._score_text(clean_q, c.name, c.description)
                if score > 0:
                    raw_results.append(
                        {
                            "score": score,
                            "item": SearchResultItem(
                                id=c.id,
                                type="course",
                                title=c.name,
                                description=c.description,
                                course_id=c.id,
                                course_name=c.name,
                            ),
                        }
                    )

        # 2. Search Units
        if not item_type or item_type.lower() == "unit":
            unit_q = self.db.query(UnitModel).join(CourseModel, UnitModel.course_id == CourseModel.id)
            if course_id:
                unit_q = unit_q.filter(UnitModel.course_id == course_id)

            for u in unit_q.all():
                score = self._score_text(clean_q, u.title, u.description)
                if score > 0:
                    raw_results.append(
                        {
                            "score": score,
                            "item": SearchResultItem(
                                id=u.id,
                                type="unit",
                                title=f"Unit {u.order_index}: {u.title}",
                                description=u.description,
                                course_id=u.course_id,
                                unit_id=u.id,
                            ),
                        }
                    )

        # 3. Search Skills
        if not item_type or item_type.lower() == "skill":
            skill_q = (
                self.db.query(SkillModel)
                .join(UnitModel, SkillModel.unit_id == UnitModel.id)
                .options(joinedload(SkillModel.lessons))
            )
            if course_id:
                skill_q = skill_q.filter(UnitModel.course_id == course_id)

            for s in skill_q.all():
                score = self._score_text(clean_q, s.title, s.description)
                if score > 0:
                    state = self.progress_service.evaluate_skill_state(current_user.id, s)
                    unit_obj = self.db.query(UnitModel).filter_by(id=s.unit_id).first()
                    raw_results.append(
                        {
                            "score": score,
                            "item": SearchResultItem(
                                id=s.id,
                                type="skill",
                                title=s.title,
                                description=s.description,
                                course_id=unit_obj.course_id if unit_obj else None,
                                unit_id=s.unit_id,
                                skill_id=s.id,
                                status=state.get("status"),
                                progress_percent=state.get("completion_percent"),
                            ),
                        }
                    )

        # 4. Search Lessons
        if not item_type or item_type.lower() == "lesson":
            lesson_q = (
                self.db.query(LessonModel)
                .join(SkillModel, LessonModel.skill_id == SkillModel.id)
                .join(UnitModel, SkillModel.unit_id == UnitModel.id)
            )
            if course_id:
                lesson_q = lesson_q.filter(UnitModel.course_id == course_id)

            for lsn in lesson_q.all():
                score = self._score_text(clean_q, lsn.title, lsn.description)
                if score > 0:
                    skill_obj = (
                        self.db.query(SkillModel)
                        .options(joinedload(SkillModel.lessons))
                        .filter_by(id=lsn.skill_id)
                        .first()
                    )
                    state = (
                        self.progress_service.evaluate_skill_state(current_user.id, skill_obj)
                        if skill_obj
                        else {"status": "available"}
                    )
                    unit_obj = (
                        self.db.query(UnitModel).filter_by(id=skill_obj.unit_id).first()
                        if skill_obj
                        else None
                    )
                    raw_results.append(
                        {
                            "score": score,
                            "item": SearchResultItem(
                                id=lsn.id,
                                type="lesson",
                                title=lsn.title,
                                description=lsn.description,
                                course_id=unit_obj.course_id if unit_obj else None,
                                unit_id=skill_obj.unit_id if skill_obj else None,
                                skill_id=lsn.skill_id,
                                status=state.get("status"),
                            ),
                        }
                    )

        # Sort by relevance score DESC, then title ASC
        sorted_items = sorted(raw_results, key=lambda r: (-r["score"], r["item"].title.lower()))
        results = [r["item"] for r in sorted_items[:limit]]

        return SearchResponse(
            query=query,
            total_results=len(sorted_items),
            results=results,
        )

    def _score_text(self, query: str, title: str, description: Optional[str] = None) -> int:
        t_low = title.lower()
        d_low = (description or "").lower()

        if t_low == query:
            return 100
        elif t_low.startswith(query):
            return 80
        elif query in t_low:
            return 60
        elif query in d_low:
            return 40
        return 0
