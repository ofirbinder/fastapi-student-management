from typing import Any, Literal

from pydantic import Field

from app.models.app_base_model import AppBaseModel


class APIResponse[T](AppBaseModel):
    status: Literal["success"] = Field("success", description="The status of the API request")
    status_code: int = Field(
        200, ge=200, le=299, description="The HTTP success status code", examples=[200, 201]
    )
    meta: dict[str, Any] | None = Field(
        None,
        description="Additional metadata (pagination, timestamps, total results, avg etc.)",
        examples=[{"count": 1, "page": 1, "avg": 86.4}],
    )
    data: T | None = Field(None, description="The actual response payload")
