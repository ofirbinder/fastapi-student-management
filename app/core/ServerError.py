from fastapi import status

from app.core.BaseError import BaseError


class ServerJsonParseError(BaseError):
    def __init__(self):
        self.message = "Invalid JSON format on server!"
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(self.message, status_code=self.status_code)
