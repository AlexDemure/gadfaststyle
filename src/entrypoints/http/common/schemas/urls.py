from pydantic import BaseModel
from pydantic import field_validator

from src.common.formats.utils import urls
from src.common.typings.validators import Link


class URL(BaseModel):
    url: Link

    @field_validator("url")
    @classmethod
    def check_url(cls, value: str) -> str:
        if not urls.safe(value):
            raise ValueError
        return value


class Photo(BaseModel):
    photo: Link

    @field_validator("photo")
    @classmethod
    def check_url(cls, value: str) -> str:
        if not urls.safe(value):
            raise ValueError
        return value
