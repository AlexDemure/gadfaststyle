import typing

from pydantic import StringConstraints


Link = typing.Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=8192,
        strip_whitespace=True,
    ),
]
