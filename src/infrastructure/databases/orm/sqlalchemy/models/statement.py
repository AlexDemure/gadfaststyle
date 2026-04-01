import typing

from pydantic import BaseModel
from sqlalchemy.sql.visitors import Visitable

from src.infrastructure.databases.orm.sqlalchemy.collections import Direction
from src.infrastructure.databases.orm.sqlalchemy.collections import Operator


class Sorting(BaseModel):
    key: str
    direction: Direction


class Pagination(BaseModel):
    limit: int
    offset: int


class Filter(BaseModel):
    key: str
    value: typing.Any
    operator: Operator


class And(BaseModel):
    filters: list[typing.Union[Filter, "And", "Or"]]


class Or(BaseModel):
    filters: list[typing.Union[Filter, "And", "Or"]]


class Function(BaseModel):
    filter: Filter
    method: typing.Callable[[Visitable], Visitable]
