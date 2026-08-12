from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UnitResponse(BaseModel):
    id: str
    course_id: str
    title: str
    description: Optional[str] = None
    order_index: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    name: str
    code: str
    source_language: str
    target_language: str
    description: Optional[str] = None


class CourseResponse(CourseBase):
    id: str
    is_active: bool
    units: List[UnitResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
