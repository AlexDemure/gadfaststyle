import typing

from pydantic import Field


Number = typing.Annotated[int, Field(ge=0)]
