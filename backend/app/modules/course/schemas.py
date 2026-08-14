from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class UnitResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: Optional[str] = None
    order_index: int

    model_config = ConfigDict(from_attributes=True)


class CourseSummaryResponse(BaseModel):
    id: str
    name: str
    code: str
    source_language: str
    target_language: str
    description: Optional[str] = None
    is_active: bool
    status: str = "available"
    total_units: int = 0
    completed_units: int = 0
    total_skills: int = 0
    completed_skills: int = 0
    total_lessons: int = 0
    completed_lessons: int = 0
    progress_percent: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class CourseDetailResponse(CourseSummaryResponse):
    units: List[UnitResponse] = []

    model_config = ConfigDict(from_attributes=True)


class SkillPathResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    xp_reward: int
    prerequisite_skill_id: Optional[str] = None
    prerequisite_title: Optional[str] = None
    status: str = "locked"  # locked, available, in_progress, completed
    completion_percent: float = 0.0
    crown_level: int = 0

    model_config = ConfigDict(from_attributes=True)


class UnitPathResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    order_index: int
    status: str = "locked"  # locked, available, in_progress, completed
    completion_percent: float = 0.0
    completed_skills: int = 0
    total_skills: int = 0
    skills: List[SkillPathResponse] = []

    model_config = ConfigDict(from_attributes=True)


class UnitProgressSummaryResponse(BaseModel):
    unit_id: str
    title: str
    status: str
    completion_percent: float
    completed_skills: int
    total_skills: int

    model_config = ConfigDict(from_attributes=True)


class CourseProgressSummaryResponse(BaseModel):
    course_id: str
    course_name: str
    status: str
    completion_percent: float
    completed_units: int
    total_units: int
    completed_skills: int
    total_skills: int
    completed_lessons: int
    total_lessons: int

    model_config = ConfigDict(from_attributes=True)


class PathResponse(BaseModel):
    course: CourseSummaryResponse
    recommended_skill_id: Optional[str] = None
    recommended_lesson_id: Optional[str] = None
    recommended_unit_id: Optional[str] = None
    units: List[UnitPathResponse] = []

    model_config = ConfigDict(from_attributes=True)
