import types

import pytest

from src.application.usecases.accounts.create import Usecase
from src.domain.collections import AccountAlreadyExists
from src.domain.models import Account
from src.infrastructure.security.jwt.models import Tokens


class AccountRepository:
    def __init__(self, exists: bool) -> None:
        self._exists = exists
        self.created: list[Account] = []

    async def exists(self, *_args, **_kwargs) -> bool:
        return self._exists

    async def create(self, model: Account) -> Account:
        self.created.append(model)
        return Account(
            id=1,
            external_id=model.external_id,
            created=model.created,
            updated=model.updated,
        )


class Encryption:
    def encrypt(self, value: str) -> str:
        return f"encrypted:{value}"


class JWT:
    def encode(self, subject: str) -> Tokens:
        return Tokens(
            access=f"access:{subject}",
            refresh=f"refresh:{subject}",
        )


def build_container(repository: AccountRepository) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        repository=types.SimpleNamespace(account=repository),
        security=types.SimpleNamespace(
            encryption=Encryption(),
            jwt=JWT(),
        ),
    )


@pytest.mark.asyncio
async def test_create_account_usecase_success(monkeypatch: pytest.MonkeyPatch) -> None:
    usecase = Usecase()
    repository = AccountRepository(exists=False)

    def build(self, _session) -> None:
        self.container = build_container(repository)

    monkeypatch.setattr(Usecase, "build", build)

    result = await Usecase.__call__.__wrapped__(usecase, object(), external_id="external-id")

    assert result == Tokens(access="access:1", refresh="refresh:1")
    assert repository.created[0].external_id == "encrypted:external-id"


@pytest.mark.asyncio
async def test_create_account_usecase_duplicate(monkeypatch: pytest.MonkeyPatch) -> None:
    usecase = Usecase()
    repository = AccountRepository(exists=True)

    def build(self, _session) -> None:
        self.container = build_container(repository)

    monkeypatch.setattr(Usecase, "build", build)

    with pytest.raises(AccountAlreadyExists):
        await Usecase.__call__.__wrapped__(usecase, object(), external_id="external-id")
