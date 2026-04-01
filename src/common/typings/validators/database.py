import typing

from pydantic import Field
from pydantic import StringConstraints


IntRef = typing.Annotated[int, Field(ge=1)]
StrRef = typing.Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=256,
        strip_whitespace=True,
    ),
]
