import typing

import jinja2

from src.common.formats.utils.string import pascal
from src.common.formats.utils.string import snake


def environment() -> jinja2.Environment:
    instance = jinja2.Environment(autoescape=False, keep_trailing_newline=True)
    instance.filters["pascal"] = pascal
    instance.filters["snake"] = snake
    return instance


def render(value: str, context: dict[str, typing.Any]) -> str:
    return environment().from_string(value).render(context)
