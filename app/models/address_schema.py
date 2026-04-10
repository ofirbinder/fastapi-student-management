from app.models.app_base_model import AppBaseModel


class AddressSchema(AppBaseModel):
    city: str
    street: str
    house_number: int
    zip_code: str
