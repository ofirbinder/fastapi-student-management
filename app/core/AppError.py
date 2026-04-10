import sys
import traceback

from app.core.config import settings

IS_PROD = settings.ENV == "production"


class AppError(Exception):
    def __init__(
        self,
        message: str | list[str],
        status_code: int,
        is_operational: bool = True,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.status = "fail" if 400 <= status_code < 500 else "error"
        self.message = message
        self.is_operational = is_operational

        if not IS_PROD:
            self.error_type = self._determine_error_type()
            self.stack_trace = self._get_stack_trace()

    def _determine_error_type(self) -> str:
        _, exc_value, _ = sys.exc_info()
        return type(exc_value).__name__ if exc_value else type(self).__name__

    def _get_stack_trace(self) -> str | None:
        return "".join(traceback.format_exc().splitlines()[-5:])

    def to_response(self):
        if IS_PROD:
            msg = "Something went very wrong!" if self.status == "error" else self.message
            return {"status": self.status, "message": msg}

        return vars(self)
