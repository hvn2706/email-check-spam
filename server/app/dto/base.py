from pydantic import BaseModel

from app.helper.utility import convert_str_to_camel


class CamelBaseModel(BaseModel):
    class Config:
        alias_generator = convert_str_to_camel
        populate_by_name = True
        