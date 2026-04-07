from datetime import date

from pydantic import BaseModel, Field

from app.models.AddressSchema import AddressSchema
from app.models.CourseSchema import CourseSchema


class StudentSchema(BaseModel):
    id: str
    name: str
    birth_date: date
    address: AddressSchema
    is_active: bool = True
    courses: list[CourseSchema] = Field(default_factory=list)
