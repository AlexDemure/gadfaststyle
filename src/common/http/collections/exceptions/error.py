import typing


class HTTPError(Exception):
    code: int

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def http(self) -> dict[str, typing.Any]:
        return dict(
            status_code=self.code,
            detail=dict(type=self.__class__.__name__),
        )
