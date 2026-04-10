from fastapi import status

from app.core.BaseError import BaseError


class DuplicateEntryError(BaseError):
    def __init__(self, message: str):
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(message=message, status_code=self.status_code)


class StudentNotExistsError(BaseError):
    def __init__(self, student_id: str):
        self.message = f"Student with this ID {student_id} does not exists on the system!"
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(message=self.message, status_code=self.status_code)


class InvalidAPIFeaturesParamsError(BaseError):
    def __init__(self, message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(message=message, status_code=self.status_code)


class StudentAlreadyEnrolledError(BaseError):
    def __init__(self, student_id: str, course_name: str | list[str]):
        self.status_code = status.HTTP_409_CONFLICT
        self.message = f"Student {student_id} is already enrolled in course{'s' if isinstance(course_name, list) and len(course_name) > 1 else ''}: {course_name}"
        super().__init__(message=self.message, status_code=self.status_code)


class InvalidActionError(BaseError):
    def __init__(self, message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(message=message, status_code=self.status_code)
