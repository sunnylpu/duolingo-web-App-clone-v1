from pydantic import BaseModel, ConfigDict


class LessonBase(BaseModel):
    title: str
    order: int
    unit_id: str


class LessonResponse(LessonBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
