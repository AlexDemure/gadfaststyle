import types

import pytest

from src.application.usecases.accounts.current import Usecase
from src.domain.collections import AccountNotFound
from src.domain.models import Account
from src.infrastructure.security.jwt.collections import TokenInvalid
from src.infrastructure.security.jwt.collections import TokenPurpose
from src.infrastructure.security.jwt.models import Token


class AccountRepository:
    def __init__(self, account: Account | None) -> None:
        self._account = account

    async def one(self, *_args, **_kwargs) -> Account:
        if not self._account:
            raise AccountNotFound
        return self._account


class Encryption:
    def decrypt(self, value: str) -> str:
        return value.removeprefix("encrypted:")


class JWT:
    def __init__(self, subject: str) -> None:
        self.subject = subject

    def decode(self, token: str, purpose: TokenPurpose) -> Token:
        assert token == "access-token"
        assert purpose is TokenPurpose.access
        return Token(
            sub=self.subject,
            purpose=purpose,
            exp=0,
            jti="jti",
        )


def build_container(repository: AccountRepository, jwt: JWT) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        repository=types.SimpleNamespace(account=repository),
        security=types.SimpleNamespace(
            encryption=Encryption(),
            jwt=jwt,
        ),
    )


@pytest.mark.asyncio
async def test_current_account_usecase_success(monkeypatch: pytest.MonkeyPatch) -> None:
    usecase = Usecase()
    repository = AccountRepository(
        Account(
            id=1,
            external_id="encrypted:external-id",
            created="2026-04-01T12:00:00+00:00",
            updated="2026-04-01T12:00:00+00:00",
        )
    )

    def build(self, _session) -> None:
        self.container = build_container(repository, JWT(subject="1"))

    monkeypatch.setattr(Usecase, "build", build)

    result = await Usecase.__call__.__wrapped__(usecase, object(), token="access-token")

    assert result.id == 1
    assert result.external_id == "external-id"


@pytest.mark.asyncio
async def test_current_account_usecase_invalid_subject(monkeypatch: pytest.MonkeyPatch) -> None:
    usecase = Usecase()
    repository = AccountRepository(account=None)

    def build(self, _session) -> None:
        self.container = build_container(repository, JWT(subject="invalid"))

    monkeypatch.setattr(Usecase, "build", build)

    with pytest.raises(TokenInvalid):
        await Usecase.__call__.__wrapped__(usecase, object(), token="access-token")
