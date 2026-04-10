from datetime import date, datetime

from pydantic import Field, ValidationInfo, field_validator

from app.models.address_schema import AddressSchema
from app.models.app_base_model import AppBaseModel
from app.models.course_schema import CourseSchema
from app.models.enums import CourseCatalog
from app.utils import validators


class StudentSchema(AppBaseModel):
    id: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description="Unique identifier for the student.",
        examples=["ST-12345"],
    )
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="The student's full name",
        examples=["Dekel Cohen"],
    )
    birth_date: date = Field(
        ..., description="Student's date of birth (YYYY-MM-DD)", examples=["1995-05-15"]
    )
    address: AddressSchema = Field(..., description="Physical residential address")
    is_active: bool = Field(
        True, description="Whether the student is currently active in the system"
    )
    courses: list[CourseSchema] = Field(
        default_factory=list,
        description=f"List of courses the student is enrolled in {[c.value for c in CourseCatalog]}",
    )
    created_at: datetime | None = Field(
        default_factory=datetime.now,
        frozen=True,
        validate_default=True,
        description="Record creation timestamp (Auto-generated, user input is ignored)",
        examples=["2026-04-10T15:30:00"],
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
