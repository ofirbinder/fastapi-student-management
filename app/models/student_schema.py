from datetime import date, datetime

from pydantic import Field, ValidationInfo, field_validator

from app.models.address_schema import AddressSchema
from app.models.app_base_model import AppBaseModel
from app.models.course_schema import CourseSchema
from app.utils import validators


class StudentSchema(AppBaseModel):
    id: str
    name: str
    birth_date: date
    address: AddressSchema
    is_active: bool = True
    courses: list[CourseSchema] = Field(default_factory=list)
    created_at: datetime | None = Field(
        default_factory=datetime.now, frozen=True, validate_default=True
    )

    @field_validator("courses")
    @classmethod
    def check_unique_courses(cls, courses: list[CourseSchema], info: ValidationInfo):
        student_id = info.data.get("id", "Unknown")
        validators.validate_no_duplicate_courses(new_courses=courses, student_id=student_id)
        return courses

    @field_validator("created_at", mode="before")
    @classmethod
    def ignore_user_input(cls, v):
        return None
