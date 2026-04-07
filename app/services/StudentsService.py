from fastapi import status
from fastapi.encoders import jsonable_encoder

from app.core.database import read_db, write_db
from app.core.DomainError import DuplicateEntryError
from app.models.APIResponse import APIResponse
from app.models.StudentSchema import StudentSchema


class StudentsService:
    @staticmethod
    def get_all_students():
        raw_data = read_db()

        students = [StudentSchema.model_validate(item) for item in raw_data]

        return APIResponse(
            data={"students": students},
            meta={"results": len(students)},
        )

    @staticmethod
    def create_student(candidate_student: StudentSchema):
        raw_data = read_db()

        if any(candidate_student.id == raw["id"] for raw in raw_data):
            raise DuplicateEntryError(candidate_student.id)

        new_student_data = jsonable_encoder(candidate_student)
        raw_data.append(new_student_data)

        write_db(raw_data)
        return APIResponse(
            status_code=status.HTTP_201_CREATED,
            data={"candidate_student": candidate_student},
        )
