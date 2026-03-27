import typing

from src.domain import models
from src.entrypoints.http.common.schemas import Paginated
from src.entrypoints.http.common.schemas import Response

from .base import System


class Account(System, Response):
    id: int
    external_id: str

    @classmethod
    def serialize(cls, account: models.Account) -> typing.Self:
        return cls(
            id=typing.cast(int, account.id),
            external_id=account.external_id,
        )


class Accounts(System, Paginated, Response):
    items: list[Account]

    @classmethod
    def serialize(cls, accounts: list[models.Account], total: int) -> typing.Self:
        return cls(
            total=total,
            items=[Account.serialize(account) for account in accounts],
        )
