from pydantic import BaseModel


class AddressSchema(BaseModel):
    city: str
    street: str
    house_number: int
    zip_code: str
