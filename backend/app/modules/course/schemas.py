from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    title: str
    source_language: str
    target_language: str


class CourseResponse(CourseBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
