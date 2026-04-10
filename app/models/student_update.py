from datetime import date

from pydantic import Field

from app.models.address_schema import AddressSchema
from app.models.app_base_model import AppBaseModel
from app.models.course_schema import CourseSchema
from app.models.enums import CourseCatalog


class StudentUpdate(AppBaseModel):
    name: str | None = Field(
        None,
        min_length=2,
        max_length=50,
        description="The student's full name",
        examples=["Aviv Galil"],
    )
    birth_date: date | None = Field(
        None, description="Student's date of birth (YYYY-MM-DD)", examples=["1995-05-15"]
    )
    address: AddressSchema | None = Field(None, description="Physical residential address")
    is_active: bool | None = Field(
        None, description="Whether the student is currently active in the system"
    )
    courses: list[CourseSchema] = Field(
        None,
        description=f"List of courses the student is enrolled in {[c.value for c in CourseCatalog]}",
    )
