import typing


def wrap(value: typing.Any) -> str:
    return f"%({value})s"
