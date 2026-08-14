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
    total_skills: int = 0
    completed_skills: int = 0
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
    skills: List[SkillPathResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PathResponse(BaseModel):
    course: CourseSummaryResponse
    recommended_skill_id: Optional[str] = None
    units: List[UnitPathResponse] = []

    model_config = ConfigDict(from_attributes=True)
