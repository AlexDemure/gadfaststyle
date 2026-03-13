import typing

from src.common.http.collections.enums.response import HTTPCode


class HTTPError(Exception):
    code: int = HTTPCode.IM_A_TEAPOT

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def http(self) -> dict[str, typing.Any]:
        return dict(
            status_code=self.code,
            detail=dict(type=self.__class__.__name__),
        )


class Forbidden(HTTPError):
    code = HTTPCode.FORBIDDEN
