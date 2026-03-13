import collections.abc
import inspect
import typing

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status


Dependency: typing.TypeAlias = typing.Callable[..., typing.Any]
Endpoint: typing.TypeAlias = tuple[str] | tuple[str, list[Dependency]]


class Health:
    def __init__(self, *endpoints: Endpoint) -> None:
        self.router = APIRouter(tags=["Health"])
        self.setup(endpoints)

    def setup(self, endpoints: collections.abc.Sequence[Endpoint]) -> None:
        for endpoint in endpoints:
            path = endpoint[0]
            depends = list(endpoint[1]) if len(endpoint) > 1 else []

            name = path.strip("/").split("/")[-1]

            self.router.add_api_route(
                path,
                self.endpoint(depends),
                description=f"Health {name} probe",
                operation_id=f"{name}_probe",
            )

    @staticmethod
    def endpoint(depends: list[Dependency]) -> typing.Callable[..., typing.Awaitable[Response]]:
        async def _endpoint(**dependencies: dict[str, typing.Any]) -> Response:
            return Response(
                status_code=status.HTTP_200_OK
                if all(bool(result) for result in dependencies.values())
                else status.HTTP_503_SERVICE_UNAVAILABLE
            )

        params = [
            inspect.Parameter(
                name=depend.__name__,
                kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=bool,
                default=Depends(depend),
            )
            for depend in depends
        ]

        setattr(_endpoint, "__signature__", inspect.Signature(params))
        return _endpoint
