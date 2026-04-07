from fastapi import APIRouter, status

from app.models.APIResponse import APIResponse
from app.models.StudentSchema import StudentSchema
from app.services import StudentsService

router = APIRouter()


@router.get(
    "/",
    response_model=APIResponse[dict[str, list[StudentSchema]]],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
def get_all_students():
    return StudentsService.get_all_students()


@router.post(
    "/",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
def create_student(student: StudentSchema):
    return StudentsService.create_student(student)
