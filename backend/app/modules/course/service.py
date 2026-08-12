from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.course.repository import CourseRepository
from app.modules.lesson.repository import LessonRepository
from app.modules.progress.repository import ProgressRepository
from app.modules.user.models import UserModel
from app.modules.course.schemas import (
    CourseSummaryResponse,
    CourseDetailResponse,
    PathResponse,
    UnitPathResponse,
    SkillPathResponse,
)
from app.shared.errors import NotFoundError


class CourseService:
    """Contains business logic for Courses and Learning Path generation."""

    def __init__(self, db: Session):
        self.db = db
        self.course_repo = CourseRepository(db)
        self.lesson_repo = LessonRepository(db)
        self.progress_repo = ProgressRepository(db)

    def get_courses(self) -> List[CourseSummaryResponse]:
        courses = self.course_repo.get_courses()
        return [CourseSummaryResponse.model_validate(c) for c in courses]

    def get_course_detail(self, course_id: str) -> CourseDetailResponse:
        course = self.course_repo.get_course_by_id(course_id)
        if not course:
            raise NotFoundError(f"Course with ID '{course_id}' was not found.")
        return CourseDetailResponse.model_validate(course)

    def get_learning_path(
        self, current_user: UserModel, course_id: Optional[str] = None
    ) -> PathResponse:
        course = None
        if course_id:
            course = self.course_repo.get_course_by_id(course_id)
        if not course:
            courses = self.course_repo.get_courses()
            if not courses:
                raise NotFoundError("No active courses available.")
            course = courses[0]

        # Fetch user's existing skill progress records
        progress_records = {
            p.skill_id: p
            for p in self.progress_repo.get_user_skill_progresses(current_user.id)
        }

        unit_paths: List[UnitPathResponse] = []
        for unit in course.units:
            skills = self.lesson_repo.get_skills_by_unit(unit.id)
            skill_paths: List[SkillPathResponse] = []

            for idx, skill in enumerate(skills):
                user_prog = progress_records.get(skill.id)

                if user_prog:
                    status = user_prog.status
                    comp_pct = user_prog.completion_percent
                    crowns = user_prog.crown_level
                else:
                    # Initial status rules: first skill or met prerequisite is available, else locked
                    if idx == 0 and unit.order_index == 1:
                        status = "available"
                    elif skill.prerequisite_skill_id and skill.prerequisite_skill_id in progress_records:
                        prereq_status = progress_records[skill.prerequisite_skill_id].status
                        status = "available" if prereq_status in ("in_progress", "completed") else "locked"
                    elif idx == 0:
                        status = "available"
                    else:
                        status = "locked"
                    comp_pct = 0.0
                    crowns = 0

                skill_paths.append(
                    SkillPathResponse(
                        id=skill.id,
                        title=skill.title,
                        description=skill.description,
                        order_index=skill.order_index,
                        xp_reward=skill.xp_reward,
                        prerequisite_skill_id=skill.prerequisite_skill_id,
                        status=status,
                        completion_percent=comp_pct,
                        crown_level=crowns,
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

        return PathResponse(
            course=CourseSummaryResponse.model_validate(course),
            units=unit_paths,
        )
