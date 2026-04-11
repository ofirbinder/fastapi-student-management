from datetime import datetime

from pydantic import Field

from app.models.student_schema import StudentSchema


class StudentInDB(StudentSchema):
    is_active: bool = Field(
        default=True,
        description="Whether the student is currently active in the system",
        validate_default=True,
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        frozen=True,
        validate_default=True,
        description="Record creation timestamp (Auto-generated, user input is ignored)",
        examples=["2026-04-10T15:30:00"],
    )
