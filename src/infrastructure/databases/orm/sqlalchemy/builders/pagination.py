import typing

from src.infrastructure.databases.orm.sqlalchemy.models import Pagination


class Builder:
    @classmethod
    def build(cls, statement: typing.Any, model: Pagination) -> typing.Any:
        return statement.limit(model.limit).offset(model.offset)
