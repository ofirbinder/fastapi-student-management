from typing import Any, Literal

from app.models.app_base_model import AppBaseModel


class APIResponse[T](AppBaseModel):
    status: Literal["success"] = "success"
    status_code: int = 200
    meta: dict[str, Any] | None = None
    data: T | None = None
