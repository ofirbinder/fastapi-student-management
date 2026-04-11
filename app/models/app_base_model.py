from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AppBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
        from_attributes=True,
        populate_by_name=True,
        alias_generator=to_camel,
    )
