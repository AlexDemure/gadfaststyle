import typing

from . import handlers


class OpenAPI:
    def __init__(self, app: typing.Any) -> None:
        self.app = app

    def generate(self) -> dict[str, typing.Any]:
        schema = typing.cast(dict[str, typing.Any], self.app.__class__.openapi(self.app))
        for handler in [handlers.affix, handlers.operationid]:
            _, schema = handler(self.app, schema)  # type: ignore
        return schema

    def __call__(self) -> dict[str, typing.Any]:
        return self.generate()
