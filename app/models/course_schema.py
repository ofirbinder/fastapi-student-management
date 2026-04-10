from pydantic import Field, computed_field

from app.models.app_base_model import AppBaseModel
from app.models.enums import CourseCatalog


class CourseSchema(AppBaseModel):
    name: CourseCatalog = Field(
        ...,
        description="The specific course name from the catalog.",
        examples=[c.value for c in CourseCatalog],
    )
    grade: int | None = Field(
        None,
        ge=0,
        le=100,
        description="Final grade. If null, the course is still in progress or not yet graded.",
        examples=[87, None],
    )

    @computed_field(
        description="Indicates if the student has successfully passed the course (Grade >= 55).",
        return_type=bool,
    )
    @property
    def is_completed(self) -> bool:
        return self.grade is not None and self.grade >= 55
