from fastapi import status
from fastapi.encoders import jsonable_encoder

from app.core.APIFeatures import APIFeatures
from app.core.database import read_db, write_db
from app.core.DomainError import DuplicateEntryError, InvalidActionError
from app.models.api_response import APIResponse
from app.models.course_schema import CourseSchema
from app.models.enums import CourseCatalog
from app.models.query_schema import QueryParams
from app.models.student_in_db import StudentInDB
from app.models.student_schema import StudentSchema
from app.models.student_update import StudentUpdate
from app.utils import validators


class StudentsService:
    @staticmethod
    def get_all_students(params: QueryParams):
        raw_data = read_db()

        validated_data = [
            StudentInDB.model_validate(item).model_dump(by_alias=False) for item in raw_data
        ]

        features = APIFeatures(validated_data, params.model_dump()).sort().paginate()

        students = features.results

        return APIResponse(
            data={"students": students},
            meta={"total": len(raw_data), "results": len(students), "page": params.page},
        )

    @staticmethod
    def get_student(id: str):
        raw_data = read_db()

        student_idx = validators.find_student_index(raw_data=raw_data, student_id=id)

        student = StudentInDB.model_validate(raw_data[student_idx])

        return APIResponse(data={"student": student})

    @staticmethod
    def create_student(student: StudentSchema):
        raw_data = read_db()

        if any(student.id == raw["id"] for raw in raw_data):
            raise DuplicateEntryError(
                f"Student with this ID {student.id}, is already exists on the system!"
            )
        full_student = StudentInDB(**student.model_dump(exclude_computed_fields=True))

        new_student_data = jsonable_encoder(full_student)
        raw_data.append(new_student_data)

        write_db(raw_data)
        return APIResponse(
            status_code=status.HTTP_201_CREATED,
            data={"student": full_student},
        )

    @staticmethod
    def add_courses(id: str, new_courses: list[CourseSchema]):
        raw_data = read_db()
        student_idx = validators.find_student_index(raw_data=raw_data, student_id=id)

        existing_courses_raw = raw_data[student_idx].get("courses", [])
        validators.validate_no_duplicate_courses(new_courses, existing_courses_raw, id)

        new_courses_encoded = jsonable_encoder(
            [course.model_dump(exclude_computed_fields=True) for course in new_courses]
        )

        raw_data[student_idx].setdefault("courses", []).extend(new_courses_encoded)
        updated_student = StudentInDB.model_validate(raw_data[student_idx])

        write_db(raw_data)

        return APIResponse(data={"student": updated_student})

    @staticmethod
    def update_student(id: str, student: StudentUpdate):
        # 1) Read the DB
        raw_data = read_db()

        # 2) Find the idx of the student by id, if not exists throw 404
        student_idx = validators.find_student_index(raw_data=raw_data, student_id=id)

        # 3) Set student to Pydantic object with model_dump(exclude_unset, exclude_computed_fields)
        update_payload = student.model_dump(
            exclude_unset=True, exclude_computed_fields=True, exclude_none=True
        )

        # 4) Verify if client ask to update courses that he didn't enrolled any course yet
        if "courses" in update_payload:
            existing_courses = raw_data[student_idx].get("courses", [])

            if len(existing_courses) > 0:
                raise InvalidActionError(
                    message=f"Cannot update courses via PATCH /students/{id}. "
                    f"Student already has enrolled courses. "
                    f"Please use POST /students/{id}/courses to add new ones."
                )
            # 4.1) Validate update_payload["courses"] has no duplicated courses!
            validators.validate_no_duplicate_courses(
                new_courses=update_payload["courses"], student_id=id
            )
            # 4.2) Turn update_payload to full Course Model to included the unset fields
            update_payload["courses"] = [
                c.model_dump(exclude_computed_fields=True) for c in student.courses
            ]

        # 6) Encoding and updating
        sanitized_update = jsonable_encoder(update_payload)
        raw_data[student_idx].update(sanitized_update)

        validated_student = StudentInDB.model_validate(raw_data[student_idx])
        # 7) Write it to DB
        write_db(raw_data)

        return APIResponse(
            data={"student": validated_student},
        )

    @staticmethod
    def delete_student(id: str):

        raw_data = read_db()

        student_idx = validators.find_student_index(raw_data=raw_data, student_id=id)

        del raw_data[student_idx]

        write_db(raw_data)

    @staticmethod
    def delete_course(id: str, course_id: CourseCatalog):
        raw_data = read_db()

        student_idx = validators.find_student_index(raw_data=raw_data, student_id=id)

        target_course = course_id.value

        existing_courses = raw_data[student_idx].get("courses", [])

        course_exists = any(course["name"] == target_course for course in existing_courses)

        if not course_exists:
            raise InvalidActionError(
                message=f"Student {id} is not enrolled in course {target_course}"
            )

        raw_data[student_idx]["courses"] = [
            course for course in existing_courses if course["name"] != target_course
        ]

        write_db(raw_data)

    # TODO
    @staticmethod
    def update_course(id: str, course_data: CourseSchema):
        raw_data = read_db()

        student_idx = validators.find_student_index(raw_data=raw_data, student_id=id)

        target_course_name = course_data.name.value

        existing_courses = raw_data[student_idx].get("courses", [])

        course_idx = next(
            (index for index, c in enumerate(existing_courses) if c["name"] == target_course_name),
            None,
        )

        if course_idx is None:
            raise InvalidActionError(
                message=f"Student {id} is not enrolled to course {target_course_name}"
            )
        updated_course_dict = jsonable_encoder(course_data.model_dump(exclude_computed_fields=True))

        raw_data[student_idx]["courses"][course_idx] = updated_course_dict
        validated_student = StudentInDB.model_validate(raw_data[student_idx])

        write_db(raw_data)

        return APIResponse(data={"student": validated_student})
