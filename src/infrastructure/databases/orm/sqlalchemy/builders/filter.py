import typing

from sqlalchemy import and_
from sqlalchemy import or_

from src.infrastructure.databases.orm.sqlalchemy.models import And
from src.infrastructure.databases.orm.sqlalchemy.models import Filter
from src.infrastructure.databases.orm.sqlalchemy.models import Or


class Builder:
    @classmethod
    def build(cls, table: typing.Any, model: typing.Union[Filter, And, Or]) -> typing.Any:
        if isinstance(model, And):
            return and_(*[cls.build(table, _model) for _model in model.filters])

        elif isinstance(model, Or):
            return or_(*[cls.build(table, _model) for _model in model.filters])

        elif isinstance(model, Filter):
            keys = model.key.split(".")

            if len(keys) > 1:
                column = getattr(table, keys[0])[keys[1]]
                method = getattr(column.astext, model.operator.value)
            else:
                column = getattr(table, keys[0])
                method = getattr(column, model.operator.value)

            if isinstance(model.value, tuple):
                return method(*model.value)
            else:
                return method(model.value)

        else:
            raise NotImplementedError
