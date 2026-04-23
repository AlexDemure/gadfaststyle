import typing

import factory


class Table(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    @classmethod
    async def init(cls, model: dict[str, typing.Any]) -> typing.Any:
        instance = cls.create(**model)
        await cls._meta.sqlalchemy_session.flush()  # type:ignore
        return instance
