import pytest

from httpx import AsyncClient
from httpx import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.databases.postgres import tables
from src.infrastructure.security.encryption import encryption
from src.infrastructure.security.jwt import jwt
from src.infrastructure.security.jwt.models import Tokens
from src.infrastructure.storages.redis import redis

from tests.factories.infrastructure.databases.postgres.tables import Account as AccountFactory
from tests.faker import fake
from tests.mocking.infrastructure.storages.redis.client import Redis


class TestDeleteCurrentAccount:
    client: AsyncClient
    session: AsyncSession
    tokens: Tokens
    external_id: str
    account_id: int

    async def setup(self) -> None:
        self.external_id = fake.uuid4()
        account = await AccountFactory.init(
            model={
                "external_id": encryption.encrypt(self.external_id),
            }
        )
        self.account_id = account.id
        self.tokens = jwt.encode(str(account.id))

    async def process(self) -> Response:
        return await self.client.delete(
            "/api/accounts:current",
            headers={"Authorization": f"Bearer {self.tokens.access}"},
        )

    async def check(self, response: Response) -> None:
        assert response.status_code == 204

        account = await self.session.scalar(select(tables.Account).where(tables.Account.id == self.account_id))

        assert account is None

    async def test(
        self,
        client: AsyncClient,
        session: AsyncSession,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self.client = client
        self.session = session

        mocked = Redis()
        monkeypatch.setattr(redis, "delete", mocked.delete)

        await self.setup()

        response = await self.process()

        await self.check(response)
