from pydantic import BaseModel, ConfigDict


class ProgressBase(BaseModel):
    user_id: str
    course_id: str
    completed_lessons: int


class ProgressResponse(ProgressBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
