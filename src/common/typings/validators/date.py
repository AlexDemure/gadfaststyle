import typing

from pydantic import Field


Year = typing.Annotated[int, Field(ge=1970)]
