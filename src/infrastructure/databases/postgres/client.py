from src.configuration import settings
from src.infrastructure.databases.orm.sqlalchemy import SQLAlchemy

from .collections import ClientDisabled


class Postgres:
    def __init__(self) -> None:
        self._orm: SQLAlchemy | None = None

    def start(self) -> None:
        if not settings.POSTGRES:
            return

        self._orm = SQLAlchemy(url=settings.asyncpg)

    def shutdown(self) -> None: ...

    @property
    def orm(self) -> SQLAlchemy:
        if not self._orm:
            raise ClientDisabled

        return self._orm
