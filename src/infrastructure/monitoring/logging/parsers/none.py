import typing

from src.infrastructure.monitoring.logging.collections import FIELD_NONE


def parser(data: typing.Any) -> typing.Any:
    if isinstance(data, dict):
        return {k: parser(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [parser(i) for i in data]
    return FIELD_NONE if data is None else data
