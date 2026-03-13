import collections.abc
import typing

from collections import Counter

from fastapi import FastAPI

from src.common.formats.utils import string
from src.framework.openapi.collections import FASTAPI_ROUTE_PATH
from src.framework.openapi.collections import SPECIFICATION_ENDPOINT
from src.framework.openapi.collections import SPECIFICATION_OPERATION_ID
from src.framework.openapi.collections import SPECIFICATION_PATHS
from src.framework.openapi.collections import SPECIFICATION_ROUTES


def handler(
    app: FastAPI,
    openapi: dict[str, typing.Any],
    exclude: collections.abc.Sequence[str] = (),
) -> tuple[FastAPI, dict[str, typing.Any]]:
    if not (routes := getattr(app, SPECIFICATION_ROUTES, [])):
        return app, openapi

    for route in routes:
        if not (_ := getattr(route, SPECIFICATION_ENDPOINT, None)):
            continue

        if path := getattr(route, FASTAPI_ROUTE_PATH, None):
            if path in exclude:
                continue

        if not (paths := openapi.get(SPECIFICATION_PATHS, {})):
            continue

        if not (methods := paths.get(path, {})):
            continue

        for method in methods:
            methods[method][SPECIFICATION_OPERATION_ID] = string.kebab(methods[method].get("description"))

    operations = []

    for path, methods in openapi.get(SPECIFICATION_PATHS, {}).items():
        for method, operation in methods.items():
            if isinstance(operation, dict):
                operations.append(methods[method][SPECIFICATION_OPERATION_ID])

    if len(operations) != len(set(operations)):
        duplicates = [operation for operation, count in Counter(operations).items() if count > 1]
        raise ValueError(f"Duplicate operationIds found: {duplicates}")

    return app, openapi
