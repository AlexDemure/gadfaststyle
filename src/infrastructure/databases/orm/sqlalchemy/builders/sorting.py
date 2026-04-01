import typing

from sqlalchemy import asc
from sqlalchemy import desc

from src.infrastructure.databases.orm.sqlalchemy.collections import Direction
from src.infrastructure.databases.orm.sqlalchemy.models import Sorting


class Builder:
    @classmethod
    def build(cls, table: typing.Any, model: Sorting) -> typing.Any:
        return asc(getattr(table, model.key)) if model.direction is Direction.asc else desc(getattr(table, model.key))
