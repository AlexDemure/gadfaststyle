import typing

from src.infrastructure.databases.orm.sqlalchemy.models import Function


class Builder:
    @classmethod
    def build(cls, table: typing.Any, model: Function) -> typing.Any:
        column = getattr(table, model.filter.key)
        function = model.method(column)
        method = getattr(function, model.filter.operator.value)
        return method(model.filter.value)
