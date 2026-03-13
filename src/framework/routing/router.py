import contextlib
import functools
import logging
import typing

from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.exceptions import ValidationException
from fastapi.routing import APIRoute
from fastapi.routing import APIRouter

from src.common.formats.utils import binary
from src.common.formats.utils import date
from src.common.formats.utils import json
from src.common.keyboard.collections import SYMBOL_DASH
from src.common.os.utils import kilobytes
from src.framework.routing.collections import Field


logger = logging.getLogger("fastapi.route")


class Logging:
    def __init__(self, request: Request) -> None:
        self.message = self.context(request)

    @classmethod
    def context(cls, request: Request) -> dict[str, typing.Any]:
        headers = dict(request.headers.items())

        return {
            Field.debug: request.app.debug,
            Field.service: request.app.title,
            Field.version: request.app.version,
            Field.http_version: request.scope.get("http_version", None),
            Field.ip: f"{request.client.host}:{request.client.port}" if request.client else None,
            Field.method: request.method.upper(),
            Field.url: str(request.url),
            Field.headers: headers,
            Field.query: dict(request.query_params),
            Field.body: {},
            Field.response: {},
            Field.code: None,
            Field.started: date.now(),
            Field.ended: None,
            Field.elapsed: None,
        }

    @property
    def endpoint(self) -> str:
        return f"{self.message[Field.method]} {self.message[Field.url]}"

    def timing(self) -> None:
        self.message[Field.ended] = date.now()
        self.message[Field.elapsed] = (self.message[Field.ended] - self.message[Field.started]).total_seconds()

    def accepted(self) -> None:
        _logger = logger.critical if self.message.get(Field.body) == SYMBOL_DASH else logger.info
        _logger(f"Request accepted - {self.endpoint}", extra=self.message)

    def processed(self) -> None:
        _logger = logger.critical if self.message.get(Field.response) == SYMBOL_DASH else logger.info
        _logger(f"Request processed - {self.endpoint}", extra=self.message)

    def error(self) -> None:
        logger.error(f"Request error - {self.endpoint}", extra=self.message, exc_info=True)


class Json:
    @classmethod
    def parse(cls, raw: bytes) -> typing.Any | str:
        with contextlib.suppress(Exception):
            return json.fromstring(binary.tostring(raw))
        return SYMBOL_DASH

    @classmethod
    def parseresponse(cls, response: Response) -> typing.Any | str:
        return cls.parse(response.body)

    @classmethod
    async def parsebody(cls, request: Request) -> typing.Any | str:
        return cls.parse(await request.body())


class Route(APIRoute):
    def get_route_handler(self) -> typing.Callable[[Request], typing.Coroutine[typing.Any, typing.Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            if route := request.scope.get("route", None):  # noqa:SIM102
                if exclude_paths := getattr(request.app, "exclude_paths", None):  # noqa:SIM102
                    if route.path_format in exclude_paths:
                        return await original_route_handler(request)

            log = Logging(request)

            if request.headers.get("Content-Type") == "application/json":
                with contextlib.suppress(ValueError):
                    log.message[Field.body] = (
                        await Json.parsebody(request)
                        if int(request.headers.get("Content-Length", 0)) < kilobytes(16)
                        else SYMBOL_DASH
                    )

            log.accepted()

            try:
                response = await original_route_handler(request)
                log.message[Field.code] = response.status_code
            except HTTPException as e:
                log.message[Field.code] = e.status_code
                log.message[Field.response] = e.detail
                log.timing()
                log.processed()
                raise e
            except ValidationException as e:
                log.message[Field.code] = status.HTTP_422_UNPROCESSABLE_ENTITY
                log.message[Field.response] = str(e)
                log.timing()
                log.processed()
                raise e
            except Exception as e:
                log.message[Field.code] = status.HTTP_500_INTERNAL_SERVER_ERROR
                log.timing()
                log.error()
                raise e

            if response.headers.get("Content-Type") == "application/json":
                log.message[Field.response] = (
                    Json.parseresponse(response) if len(response.body) < kilobytes(64) else SYMBOL_DASH
                )

            log.timing()
            log.processed()

            return response

        return custom_route_handler


Router = functools.partial(APIRouter, route_class=Route)
