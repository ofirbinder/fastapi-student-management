from pydantic import BaseModel, Field


class CourseSchema(BaseModel):
    name: str
    grade: int = Field(ge=0, le=100)
