import typing

from pydantic import BaseModel
from pydantic import ConfigDict


class Base(BaseModel):
    __encrypted__: list[str] = []

    model_config = ConfigDict(from_attributes=True, extra="allow")

    @classmethod
    def init(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        raise NotImplementedError

    @classmethod
    def encrypt(cls, encrypter: typing.Callable[..., typing.Any], **kwargs: typing.Any) -> dict[str, typing.Any]:
        payload = dict()

        for key, value in kwargs.items():
            if key in cls.__encrypted__:
                if value:
                    payload[key] = encrypter(value)
                else:
                    payload[key] = None

        return payload

    @classmethod
    def decrypt(cls, decrypter: typing.Callable[..., typing.Any], **kwargs: typing.Any) -> dict[str, typing.Any]:
        payload = dict()

        for key, value in kwargs.items():
            if key in cls.__encrypted__:
                if value:
                    payload[key] = decrypter(value)
                else:
                    payload[key] = None
        return payload


Model = typing.TypeVar("Model", bound=Base)
