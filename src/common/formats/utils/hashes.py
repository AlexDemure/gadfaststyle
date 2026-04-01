import hashlib
import typing

from pydantic import BaseModel

from . import json


def deterministic(func: typing.Callable[..., typing.Any], context: dict[str, typing.Any] | None = None) -> str:
    params: dict[str, typing.Any] = (
        {
            name: value
            for name, value in context.items()
            if isinstance(value, (str, int, float, bool, list, dict, tuple, BaseModel, type(None)))
        }
        if context
        else {}
    )
    data: dict[str, typing.Any] = {
        "func": f"{func.__module__}.{func.__name__}",
        "params": dict(sorted(params.items())),
    }
    return hashlib.md5(json.tostring(data, sort_keys=True).encode()).hexdigest()
