import functools
import typing


def decorator(handler: typing.Any) -> typing.Any:
    @functools.wraps(handler)
    async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        if kwargs.get("account"):
            return await handler(*args, **kwargs)
        return None

    return wrapper
