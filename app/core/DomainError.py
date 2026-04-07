from fastapi import status

from app.core.BaseError import BaseError


class DuplicateEntryError(BaseError):
    def __init__(self, student_id: str):
        self.message = f"Student with this ID {student_id}, is already exists on the system!"
        self.status_code = status.HTTP_409_CONFLICT
        super().__init__(message=self.message, status_code=status.HTTP_409_CONFLICT)
