import typing

from src.infrastructure.monitoring.logging.collections import FIELD_HIDDEN


def parser(data: typing.Any, hidden: list[str]) -> typing.Any:
    if isinstance(data, dict):
        return {k: (FIELD_HIDDEN if k.lower() in hidden else parser(v, hidden)) for k, v in data.items()}
    elif isinstance(data, list):
        return [parser(i, hidden) for i in data]
    return data
