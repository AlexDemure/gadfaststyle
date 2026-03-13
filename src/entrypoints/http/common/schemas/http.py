import typing

from src.framework.openapi.models import Affix


class Request(Affix):
    __affix__ = "Request:"

    def deserialize(self, *args: typing.Any, **kwargs: typing.Any) -> dict[str, typing.Any]:
        return self.model_dump()


class Response(Affix):
    __affix__ = "Response:"

    def serialize(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        raise NotImplementedError
