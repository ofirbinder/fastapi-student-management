from fastapi import APIRouter, Body, Depends, Path, status

from app.models.api_response import APIResponse
from app.models.course_schema import CourseSchema
from app.models.enums import CourseCatalog
from app.models.query_params import QueryParams
from app.models.student_schema import StudentSchema
from app.models.student_update import StudentUpdate
from app.services import StudentsService

router = APIRouter()


@router.get(
    "/",
    response_model=APIResponse[dict[str, list[StudentSchema]]],
    status_code=status.HTTP_200_OK,
    # response_model_exclude_none=True,
)
def get_all_students(query_params: QueryParams = Depends()):
    return StudentsService.get_all_students(query_params)


@router.get(
    "/{id}",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    # response_model_exclude_none=True,
)
def get_student(id: str = Path(...)):
    return StudentsService.get_student(id)


@router.post(
    "/",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_201_CREATED,
    # response_model_exclude_none=True,
)
def create_student(student: StudentSchema):
    return StudentsService.create_student(student)


@router.post(
    "/{id}/courses",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    # response_model_exclude_none=True,
)
def add_courses(
    id: str = Path(...), courses: CourseSchema | list[CourseSchema] = Body(..., embed=True)
):
    return StudentsService.add_courses(id, courses)


@router.patch(
    "/{id}",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    # response_model_exclude_none=True,
)
def update_student(id: str = Path(...), student_data: StudentUpdate = Body(...)):
    return StudentsService.update_student(id, student_data)


@router.patch(
    "/{id}/courses",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    # response_model_exclude_none=True,
)
def update_course(id: str = Path(...), course_data: CourseSchema = Body(..., embed=True)):
    return StudentsService.update_course(id, course_data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(id: str = Path(...)):
    StudentsService.delete_student(id)


@router.delete(
    "/{id}/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_course_from_student(id: str = Path(...), course_id: CourseCatalog = Path(...)):
    StudentsService.delete_course(id, course_id)
