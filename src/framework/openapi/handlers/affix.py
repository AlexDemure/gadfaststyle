import typing

from fastapi import FastAPI

from src.framework.openapi.collections import SPECIFICATION_COMPONENTS
from src.framework.openapi.collections import SPECIFICATION_COMPONENTS_SCHEMAS
from src.framework.openapi.collections import SPECIFICATION_COMPONENTS_SCHEMAS_TITLE
from src.framework.openapi.utils import findrefs


def handler(app: FastAPI, openapi: dict[str, typing.Any]) -> tuple[FastAPI, dict[str, typing.Any]]:
    updated: dict[str, typing.Any] = {}
    mapped: dict[str, str] = {}

    if not (components := openapi.get(SPECIFICATION_COMPONENTS)):
        return app, openapi

    schemas = components.get(SPECIFICATION_COMPONENTS_SCHEMAS, {})

    for key, schema in schemas.items():
        title = schema.get(SPECIFICATION_COMPONENTS_SCHEMAS_TITLE, key)
        if title != key:
            mapped[key] = title
        updated[title] = schema

    components[SPECIFICATION_COMPONENTS_SCHEMAS] = dict(sorted(updated.items()))

    for key, title in mapped.items():
        findrefs(openapi, key, title)

    return app, openapi
