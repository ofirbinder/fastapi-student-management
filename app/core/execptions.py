import json

import portalocker
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core import BaseError
from app.core.AppError import AppError
from app.core.DomainError import (
    DuplicateEntryError,
    InvalidActionError,
    InvalidAPIFeaturesParamsError,
    StudentAlreadyEnrolledError,
    StudentNotExistsError,
)
from app.core.ServerError import ServerJsonParseError


async def domain_error_handler(_request: Request, _exc: BaseError):
    error = AppError(status_code=_exc.status_code, message=getattr(_exc, "message", str(_exc)))
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def file_system_error_handler(_request: Request, _exc: OSError):
    messages = {
        FileNotFoundError: "Database file is missing on the server!",
        PermissionError: "Server has no permission to read the database!",
        IsADirectoryError: "Database path is a directory!",
    }

    msg = messages.get(type(_exc), "A file system error occurred.")
    error = AppError(status_code=500, message=msg, is_operational=False)
    return JSONResponse(status_code=500, content=error.to_response())


def setup_exception_handlers(app: FastAPI):
    domain_errors = [
        DuplicateEntryError,
        StudentNotExistsError,
        InvalidAPIFeaturesParamsError,
        StudentAlreadyEnrolledError,
        InvalidActionError,
        ServerJsonParseError,
    ]
    for err in domain_errors:
        app.add_exception_handler(err, domain_error_handler)

    for err in [FileNotFoundError, PermissionError, IsADirectoryError]:
        app.add_exception_handler(err, file_system_error_handler)

    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(PydanticValidationError, validation_handler)
    app.add_exception_handler(json.JSONDecodeError, invalid_json_handler)
    app.add_exception_handler(portalocker.exceptions.LockException, file_locked_handler)
    app.add_exception_handler(StarletteHTTPException, http_exc_handler)


##################################################
##################################################


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
    error = AppError(
        status_code=status_code,
        message="Database is temporarily locked. Please try again.",
        is_operational=False,
    )
    return JSONResponse(status_code=error.status_code, content=error.to_response())


async def http_exc_handler(_request: Request, _exc: StarletteHTTPException):
    error = AppError(status_code=_exc.status_code, message=_exc.detail)
    return JSONResponse(status_code=error.status_code, content=error.to_response())
