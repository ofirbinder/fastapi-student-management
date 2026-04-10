from pydantic import BaseModel, ConfigDict


class AppBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True, from_attributes=True)
