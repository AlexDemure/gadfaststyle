import typing

from sqlalchemy import func

from src.infrastructure.databases.orm.sqlalchemy import models
from src.infrastructure.databases.orm.sqlalchemy.collections import Direction
from src.infrastructure.databases.orm.sqlalchemy.collections import Operator


class JSONBArray:
    @classmethod
    def gt(cls, key: str, value: typing.Any) -> models.Function:
        return models.Function(filter=Comparison.gt(key=key, value=value), method=func.jsonb_array_length)


class Array:
    @staticmethod
    def in_(key: str, values: list[typing.Any]) -> models.Filter:
        return models.Filter(key=key, operator=Operator.in_, value=list(values))

    @staticmethod
    def int_(key: str, values: list[typing.Any]) -> models.Filter:
        return models.Filter(key=key, operator=Operator.int_, value=list(values))


class Range:
    @staticmethod
    def between(key: str, value: tuple[typing.Any, typing.Any]) -> models.Filter:
        return models.Filter(key=key, operator=Operator.between, value=value)


class Search:
    @staticmethod
    def like(key: str, value: str) -> models.Filter:
        return models.Filter(key=key, operator=Operator.like, value=value)


class Comparison:
    @staticmethod
    def eq(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.eq, value=value)

    @staticmethod
    def ne(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.ne, value=value)

    @staticmethod
    def gt(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.gt, value=value)

    @staticmethod
    def gte(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.gte, value=value)

    @staticmethod
    def lt(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.lt, value=value)

    @staticmethod
    def lte(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.lte, value=value)

    @staticmethod
    def is_(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.is_, value=value)

    @staticmethod
    def ist_(key: str, value: typing.Any) -> models.Filter:
        return models.Filter(key=key, operator=Operator.ist_, value=value)


class Filter(Array, Range, Search, Comparison): ...


class Pagination:
    @staticmethod
    def page(limit: int, offset: int = 0) -> models.Pagination:
        return models.Pagination(limit=limit, offset=offset)


class Sorting:
    @staticmethod
    def asc(key: str) -> models.Sorting:
        return models.Sorting(key=key, direction=Direction.asc)

    @staticmethod
    def desc(key: str) -> models.Sorting:
        return models.Sorting(key=key, direction=Direction.desc)


class And:
    @classmethod
    def combine(cls, *filters: typing.Union[models.Filter, models.And, models.Or]) -> models.And:
        return models.And(filters=list(filters))


class Or:
    @classmethod
    def combine(cls, *filters: typing.Union[models.Filter, models.And, models.Or]) -> models.Or:
        return models.Or(filters=list(filters))
