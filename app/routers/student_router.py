from fastapi import APIRouter, Body, Depends, Path, status

from app.models.api_response import APIResponse
from app.models.course_schema import CourseSchema
from app.models.enums import CourseCatalog
from app.models.query_schema import QueryParams
from app.models.student_schema import StudentSchema
from app.models.student_update import StudentUpdate
from app.services import StudentsService

router = APIRouter()


@router.get(
    "/",
    response_model=APIResponse[dict[str, list[StudentSchema]]],
    status_code=status.HTTP_200_OK,
    summary="Get all students",
    description="Retrieve a paginated and sorted list of all students.",
)
def get_all_students(query_params: QueryParams = Depends()):
    return StudentsService.get_all_students(query_params)


@router.get(
    "/{id}",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    summary="Get student by ID",
)
def get_student(id: str = Path(...)):
    return StudentsService.get_student(id)


@router.post(
    "/",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
    description="Registers a new student in the system with their address and initial courses.",
)
def create_student(student: StudentSchema):
    return StudentsService.create_student(student)


@router.post(
    "/{id}/courses",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    summary="Add courses to student",
    description="Add one or multiple courses to an existing student's record.",
)
def add_courses(id: str = Path(...), courses: list[CourseSchema] = Body(...)):
    return StudentsService.add_courses(id, courses)


@router.patch(
    "/{id}",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    summary="Update student details",
    description="Partially update student information like name or address.",
)
def update_student(id: str = Path(...), student_data: StudentUpdate = Body(...)):
    return StudentsService.update_student(id, student_data)


@router.patch(
    "/{id}/courses",
    response_model=APIResponse[dict[str, StudentSchema]],
    status_code=status.HTTP_200_OK,
    summary="Update student course",
    description="Update of a specific course for a student.",
)
def update_course(id: str = Path(...), course_data: CourseSchema = Body(...)):
    return StudentsService.update_course(id, course_data)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student",
    description="Permanently remove a student and all their associated data from the system.",
)
def delete_student(id: str = Path(...)):
    StudentsService.delete_student(id)


@router.delete(
    "/{id}/courses/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a course from student",
    description="Remove a specific course enrollment from a student's profile.",
)
def delete_course_from_student(id: str = Path(...), course_id: CourseCatalog = Path(...)):
    StudentsService.delete_course(id, course_id)
