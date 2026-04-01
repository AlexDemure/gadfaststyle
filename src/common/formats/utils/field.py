import contextlib
import typing


def required(field: typing.Any) -> typing.Any:
    if not field:
        raise ValueError("Field is required")
    return field


def safe(
    func: typing.Callable[..., typing.Any],
    *args: typing.Any,
    **kwargs: typing.Any,
) -> typing.Any | None:
    with contextlib.suppress(Exception):
        return func(*args, **kwargs)
    return None
