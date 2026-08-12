from typing import List, Optional
from app.modules.lesson.repository import LessonRepository
from app.modules.lesson.models import SkillModel, LessonModel, ExerciseModel


class LessonService:
    """Contains business logic for Skills, Lessons, and Exercises."""

    def __init__(self, repository: LessonRepository):
        self.repository = repository

    def list_lessons(self) -> List[LessonModel]:
        return self.repository.db.query(LessonModel).all()

    def get_skill(self, skill_id: str) -> Optional[SkillModel]:
        return self.repository.get_skill_by_id(skill_id)

    def get_lesson(self, lesson_id: str) -> Optional[LessonModel]:
        return self.repository.get_lesson_by_id(lesson_id)

    def get_lesson_exercises(self, lesson_id: str) -> List[ExerciseModel]:
        return self.repository.get_exercises_by_lesson(lesson_id)
