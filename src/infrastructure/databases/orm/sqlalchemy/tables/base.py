import typing

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


Table = typing.TypeVar("Table", bound=Base)
