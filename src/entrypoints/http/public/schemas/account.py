import datetime
import typing

from src.common.formats.utils import field
from src.domain.models import Account as Model
from src.entrypoints.http.common.schemas import Command
from src.entrypoints.http.common.schemas import Query
from src.entrypoints.http.common.schemas import Request
from src.entrypoints.http.common.schemas import Response

from .base import Public


class CreateAccount(Public, Request, Command):
    external_id: str


class CurrentAccount(Public, Response, Query):
    id: int
    external_id: str
    created: datetime.datetime
    updated: datetime.datetime

    @classmethod
    def serialize(cls, model: Model) -> typing.Self:
        return cls(
            id=field.required(model.id),
            external_id=model.external_id,
            created=model.created,
            updated=model.updated,
        )
