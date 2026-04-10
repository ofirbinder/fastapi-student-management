from pydantic import Field

from app.models.app_base_model import AppBaseModel


class QueryParams(AppBaseModel):
    page: int = Field(1, gt=0)
    limit: int = Field(10, gt=0, le=100)
    sort_by: str | None = None
