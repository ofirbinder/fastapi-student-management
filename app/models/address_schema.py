from pydantic import Field

from app.models.app_base_model import AppBaseModel


class AddressSchema(AppBaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="The name of the city",
        examples=["Haifa", "Tel Aviv", "Herzeliya"],
    )
    street: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="The name of the street",
        examples=["Moshe Goshen", "Ahi Eilat"],
    )
    house_number: int = Field(
        ...,
        gt=0,
        lt=100000,
        description="The physical house number on the street",
        examples=[58, 68],
    )
    zip_code: str = Field(
        ...,
        pattern=r"^\d{7}$",
        description="Israeli postal code (exactly 7 digits)",
        examples=["2625102", "3467901"],
    )
