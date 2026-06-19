import typing

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __tablename__: str
    __collection__: str


Table = typing.TypeVar("Table", bound=Base)
