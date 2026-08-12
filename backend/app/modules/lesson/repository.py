from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.lesson.models import SkillModel, LessonModel, ExerciseModel


class LessonRepository:
    """Handles data persistence for Skills, Lessons, and Exercises."""

    def __init__(self, db: Session):
        self.db = db

    def get_skill_by_id(self, skill_id: str) -> Optional[SkillModel]:
        return self.db.query(SkillModel).filter(SkillModel.id == skill_id).first()

    def get_skills_by_unit(self, unit_id: str) -> List[SkillModel]:
        return (
            self.db.query(SkillModel)
            .filter(SkillModel.unit_id == unit_id)
            .order_by(SkillModel.order_index)
            .all()
        )

    def create_or_update_skill(
        self,
        skill_id: str,
        unit_id: str,
        title: str,
        description: Optional[str] = None,
        order_index: int = 1,
        xp_reward: int = 10,
        prerequisite_skill_id: Optional[str] = None,
    ) -> SkillModel:
        skill = self.get_skill_by_id(skill_id)
        if not skill:
            skill = SkillModel(
                id=skill_id,
                unit_id=unit_id,
                title=title,
                description=description,
                order_index=order_index,
                xp_reward=xp_reward,
                prerequisite_skill_id=prerequisite_skill_id,
            )
            self.db.add(skill)
        else:
            skill.unit_id = unit_id
            skill.title = title
            skill.description = description
            skill.order_index = order_index
            skill.xp_reward = xp_reward
            skill.prerequisite_skill_id = prerequisite_skill_id

        self.db.commit()
        self.db.refresh(skill)
        return skill

    def get_lesson_by_id(self, lesson_id: str) -> Optional[LessonModel]:
        return self.db.query(LessonModel).filter(LessonModel.id == lesson_id).first()

    def get_lessons_by_skill(self, skill_id: str) -> List[LessonModel]:
        return (
            self.db.query(LessonModel)
            .filter(LessonModel.skill_id == skill_id)
            .order_by(LessonModel.order_index)
            .all()
        )

    def create_or_update_lesson(
        self,
        lesson_id: str,
        skill_id: str,
        title: str,
        description: Optional[str] = None,
        order_index: int = 1,
        xp_reward: int = 10,
        estimated_minutes: int = 5,
    ) -> LessonModel:
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson:
            lesson = LessonModel(
                id=lesson_id,
                skill_id=skill_id,
                title=title,
                description=description,
                order_index=order_index,
                xp_reward=xp_reward,
                estimated_minutes=estimated_minutes,
            )
            self.db.add(lesson)
        else:
            lesson.skill_id = skill_id
            lesson.title = title
            lesson.description = description
            lesson.order_index = order_index
            lesson.xp_reward = xp_reward
            lesson.estimated_minutes = estimated_minutes

        self.db.commit()
        self.db.refresh(lesson)
        return lesson

    def get_exercise_by_id(self, exercise_id: str) -> Optional[ExerciseModel]:
        return self.db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()

    def get_exercises_by_lesson(self, lesson_id: str) -> List[ExerciseModel]:
        return (
            self.db.query(ExerciseModel)
            .filter(ExerciseModel.lesson_id == lesson_id)
            .order_by(ExerciseModel.order_index)
            .all()
        )

    def create_or_update_exercise(
        self,
        exercise_id: str,
        lesson_id: str,
        type: str,
        prompt: str,
        correct_answer: str,
        data: Optional[dict] = None,
        order_index: int = 1,
        xp_reward: int = 5,
    ) -> ExerciseModel:
        exercise = self.get_exercise_by_id(exercise_id)
        if not exercise:
            exercise = ExerciseModel(
                id=exercise_id,
                lesson_id=lesson_id,
                type=type,
                prompt=prompt,
                correct_answer=correct_answer,
                data=data,
                order_index=order_index,
                xp_reward=xp_reward,
            )
            self.db.add(exercise)
        else:
            exercise.lesson_id = lesson_id
            exercise.type = type
            exercise.prompt = prompt
            exercise.correct_answer = correct_answer
            exercise.data = data
            exercise.order_index = order_index
            exercise.xp_reward = xp_reward

        self.db.commit()
        self.db.refresh(exercise)
        return exercise
