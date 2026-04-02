import types

import pytest

from src.application.usecases.accounts.delete import Usecase
from src.domain.collections import AccountNotFound
from src.infrastructure.security.jwt.collections import TokenInvalid
from src.infrastructure.security.jwt.collections import TokenPurpose
from src.infrastructure.security.jwt.models import Token


class AccountRepository:
    def __init__(self, exists: bool = True) -> None:
        self._exists = exists
        self.deleted = False

    async def one(self, *_args, **_kwargs) -> None:
        if not self._exists:
            raise AccountNotFound

    async def delete(self, *_args, **_kwargs) -> None:
        self.deleted = True


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
        security=types.SimpleNamespace(jwt=jwt),
    )


@pytest.mark.asyncio
async def test_delete_account_usecase_success(monkeypatch: pytest.MonkeyPatch) -> None:
    usecase = Usecase()
    repository = AccountRepository(exists=True)

    def build(self, _session) -> None:
        self.container = build_container(repository, JWT(subject="1"))

    monkeypatch.setattr(Usecase, "build", build)

    await Usecase.__call__.__wrapped__(usecase, object(), token="access-token")

    assert repository.deleted is True


@pytest.mark.asyncio
async def test_delete_account_usecase_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    usecase = Usecase()
    repository = AccountRepository(exists=False)

    def build(self, _session) -> None:
        self.container = build_container(repository, JWT(subject="1"))

    monkeypatch.setattr(Usecase, "build", build)

    with pytest.raises(AccountNotFound):
        await Usecase.__call__.__wrapped__(usecase, object(), token="access-token")

    assert repository.deleted is False


@pytest.mark.asyncio
async def test_delete_account_usecase_invalid_subject(monkeypatch: pytest.MonkeyPatch) -> None:
    usecase = Usecase()
    repository = AccountRepository()

    def build(self, _session) -> None:
        self.container = build_container(repository, JWT(subject="invalid"))

    monkeypatch.setattr(Usecase, "build", build)

    with pytest.raises(TokenInvalid):
        await Usecase.__call__.__wrapped__(usecase, object(), token="access-token")
