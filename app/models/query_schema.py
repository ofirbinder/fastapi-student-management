from pydantic import Field

from app.models.app_base_model import AppBaseModel


class QueryParams(AppBaseModel):
    page: int = Field(1, gt=0, description="The page number to retrieve.", examples=[1, 4])
    limit: int = Field(
        10, gt=0, le=100, description="Number of records per page (max 100).", examples=[3, 5, 20]
    )
    sort_by: str | None = Field(
        None,
        description=(
            "The field to sort by. Use a minus sign ('-') for descending order (e.g., '-name'). "
            "Supported fields: id, name, birth_date, is_active, created_at."
        ),
        examples=["name", "-created_at"],
    )
