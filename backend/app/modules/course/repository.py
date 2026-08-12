from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.course.models import CourseModel, UnitModel


class CourseRepository:
    """Handles data persistence for the Course domain."""

    def __init__(self, db: Session):
        self.db = db

    def get_courses(self, skip: int = 0, limit: int = 100) -> List[CourseModel]:
        return self.db.query(CourseModel).filter(CourseModel.is_active == True).offset(skip).limit(limit).all()

    def get_course_by_id(self, course_id: str) -> Optional[CourseModel]:
        return self.db.query(CourseModel).filter(CourseModel.id == course_id).first()

    def get_course_by_code(self, code: str) -> Optional[CourseModel]:
        return self.db.query(CourseModel).filter(CourseModel.code == code).first()

    def create_or_update_course(
        self,
        course_id: str,
        name: str,
        code: str,
        source_language: str,
        target_language: str,
        description: Optional[str] = None,
    ) -> CourseModel:
        course = self.get_course_by_id(course_id) or self.get_course_by_code(code)
        if not course:
            course = CourseModel(
                id=course_id,
                name=name,
                code=code,
                source_language=source_language,
                target_language=target_language,
                description=description,
            )
            self.db.add(course)
        else:
            course.name = name
            course.code = code
            course.source_language = source_language
            course.target_language = target_language
            course.description = description

        self.db.commit()
        self.db.refresh(course)
        return course

    def get_units_by_course(self, course_id: str) -> List[UnitModel]:
        return (
            self.db.query(UnitModel)
            .filter(UnitModel.course_id == course_id)
            .order_by(UnitModel.order_index)
            .all()
        )

    def get_unit_by_id(self, unit_id: str) -> Optional[UnitModel]:
        return self.db.query(UnitModel).filter(UnitModel.id == unit_id).first()

    def create_or_update_unit(
        self,
        unit_id: str,
        course_id: str,
        title: str,
        description: Optional[str] = None,
        order_index: int = 1,
    ) -> UnitModel:
        unit = self.get_unit_by_id(unit_id)
        if not unit:
            unit = UnitModel(
                id=unit_id,
                course_id=course_id,
                title=title,
                description=description,
                order_index=order_index,
            )
            self.db.add(unit)
        else:
            unit.course_id = course_id
            unit.title = title
            unit.description = description
            unit.order_index = order_index

        self.db.commit()
        self.db.refresh(unit)
        return unit
