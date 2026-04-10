import json

import portalocker
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.AppError import AppError
from app.core.DomainError import (
    DuplicateEntryError,
    InvalidActionError,
    InvalidAPIFeaturesParamsError,
    StudentAlreadyEnrolledError,
    StudentNotExistsError,
)
from app.core.ServerError import ServerJsonParseError


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(json.JSONDecodeError, invalid_json_handler)
    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(PydanticValidationError, validation_handler)
    app.add_exception_handler(portalocker.exceptions.LockException, file_locked_handler)
    app.add_exception_handler(StarletteHTTPException, http_exc_handler)

    app.add_exception_handler(DuplicateEntryError, duplicate_entry_handler)
    app.add_exception_handler(ServerJsonParseError, server_json_invalid_handler)
    app.add_exception_handler(StudentNotExistsError, student_not_exists_handler)
    app.add_exception_handler(InvalidAPIFeaturesParamsError, invalid_params_handler)
    app.add_exception_handler(StudentAlreadyEnrolledError, duplicate_course_handler)
    app.add_exception_handler(InvalidActionError, invalid_action_handler)

    app.add_exception_handler(FileNotFoundError, file_not_found_handler)
    app.add_exception_handler(PermissionError, permission_denied_handler)
    app.add_exception_handler(IsADirectoryError, is_directory_handler)


async def invalid_action_handler(_request: Request, _exc: InvalidActionError):
    error = AppError(status_code=_exc.status_code, message=_exc.message)
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def duplicate_course_handler(_request: Request, _exc: StudentAlreadyEnrolledError):
    error = AppError(status_code=_exc.status_code, message=_exc.message)
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def invalid_params_handler(_request: Request, _exc: InvalidAPIFeaturesParamsError):
    error = AppError(status_code=_exc.status_code, message=_exc.message)
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def student_not_exists_handler(_request: Request, _exc: StudentNotExistsError):
    error = AppError(status_code=_exc.status_code, message=_exc.message)
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def server_json_invalid_handler(_request: Request, _exc: ServerJsonParseError):
    error = AppError(status_code=_exc.status_code, message=_exc.message)
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def invalid_json_handler(_request: Request, _exc: json.JSONDecodeError):
    error = AppError(
        message="Invalid JSON format. Please check your syntax.",
        status_code=status.HTTP_400_BAD_REQUEST,
    )
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def validation_handler(
    _request: Request, _exc: RequestValidationError | PydanticValidationError
):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    is_operational = True

    if not isinstance(_exc, RequestValidationError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        is_operational = False

    error_messages = []
    is_json_syntax_error = False

    for error in _exc.errors():
        if error.get("type") == "json_invalid":
            is_json_syntax_error = True
            break

        field = " -> ".join([str(err) for err in error["loc"] if err != "body"])
        msg = error.get("msg", "Invalid value")
        error_messages.append(f"{field}: {msg}" if field else msg)

    if is_json_syntax_error:
        status_code = status.HTTP_400_BAD_REQUEST
        final_message = "Invalid JSON syntax. Please check for missing commas or brackets."
    else:
        final_message = error_messages if error_messages else "Validation failed"

    error = AppError(message=final_message, status_code=status_code, is_operational=is_operational)

    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def file_locked_handler(_request: Request, _exc: portalocker.exceptions.LockException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    error = AppError(status_code=status_code, message=_exc.detail, is_operational=False)
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def file_not_found_handler(_request: Request, _exc: FileNotFoundError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = AppError(
        status_code=status_code,
        message="Database file is missing on the server! Please try again later.",
        is_operational=False,
    )
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def permission_denied_handler(_request: Request, _exc: PermissionError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = AppError(
        status_code=status_code,
        message="Server has no permission to read the database! Please try again later.",
        is_operational=False,
    )
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def is_directory_handler(_request: Request, _exc: IsADirectoryError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = AppError(
        status_code=status_code, message="Database path is a directory! Please try again later."
    )
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def http_exc_handler(_request: Request, _exc: StarletteHTTPException):
    error = AppError(status_code=_exc.status_code, message=_exc.detail)
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def duplicate_entry_handler(_request: Request, _exc: DuplicateEntryError):
    error = AppError(status_code=_exc.status_code, message=_exc.message)
    return JSONResponse(status_code=error.status_code, content=error.to_response())
