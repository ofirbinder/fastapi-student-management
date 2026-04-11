from app.core.DomainError import (
    DuplicateEntryError,
    StudentAlreadyEnrolledError,
    StudentNotExistsError,
)


def validate_no_duplicate_courses(
    new_courses: list, existing_courses: list = None, student_id: str = "Unknown"
):
    if existing_courses is None:
        existing_courses = []

    seen = set()
    input_duplicates = []

    for course in new_courses:
        if isinstance(course, dict):
            name = course.get("name")
        else:
            name = course.name.value if hasattr(course.name, "value") else course.name

        if name in seen:
            input_duplicates.append(name)
        seen.add(name)

    if input_duplicates:
        raise DuplicateEntryError(
            f"Input error: The following courses appear multiple times in your request: {input_duplicates}"
        )

    existing_names = {
        c["name"] if isinstance(c, dict) else (c.name.value if hasattr(c.name, "value") else c.name)
        for c in existing_courses
    }

    existing_duplicates = [name for name in seen if name in existing_names]

    if existing_duplicates:
        raise StudentAlreadyEnrolledError(student_id, existing_duplicates)


def find_student_index(raw_data: list, student_id: str) -> int:
    idx = next((i for i, s in enumerate(raw_data) if s["id"] == student_id), None)
    if idx is None:
        raise StudentNotExistsError(student_id)
    return idx
