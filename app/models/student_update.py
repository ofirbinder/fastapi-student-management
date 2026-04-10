from datetime import date

from app.models.address_schema import AddressSchema
from app.models.app_base_model import AppBaseModel
from app.models.course_schema import CourseSchema


class StudentUpdate(AppBaseModel):
    name: str | None = None
    birth_date: date | None = None
    address: AddressSchema | None = None
    is_active: bool | None = None
    courses: list[CourseSchema] = None
