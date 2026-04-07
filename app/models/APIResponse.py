from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class APIResponse[T](BaseModel):
    model_config = ConfigDict(exclude_none=True)
    status: Literal["success"] = "success"
    status_code: int = 200
    meta: dict[str, Any] | None = None
    data: T | None = None
