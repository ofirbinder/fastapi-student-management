from pydantic import Field, computed_field

from app.models.app_base_model import AppBaseModel
from app.models.enums import CourseCatalog


class CourseSchema(AppBaseModel):
    name: CourseCatalog
    grade: int | None = Field(None, ge=0, le=100)

    @computed_field
    @property
    def is_completed(self) -> bool:
        return self.grade is not None and self.grade >= 55
