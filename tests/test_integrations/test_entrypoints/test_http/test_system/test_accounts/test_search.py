import datetime

import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.formats.utils import date
from src.configuration import settings
from src.infrastructure.security.encryption import encryption

from tests.factories.infrastructure.databases.postgres import tables
from tests.faker import fake


class TestAccountsSearch:
    @pytest.fixture(autouse=True)
    async def setup(self, client: AsyncClient, session: AsyncSession) -> None:
        self.client = client
        self.session = session

        self.authentication = settings.AUTHENTICATION
        self.username = settings.AUTHENTICATION_HTTP_BASIC_USERNAME
        self.password = settings.AUTHENTICATION_HTTP_BASIC_PASSWORD

        settings.AUTHENTICATION = True
        settings.AUTHENTICATION_HTTP_BASIC_USERNAME = "admin"
        settings.AUTHENTICATION_HTTP_BASIC_PASSWORD = "password"

    @pytest.fixture(autouse=True)
    async def teardown(self) -> None:
        yield

        settings.AUTHENTICATION = self.authentication
        settings.AUTHENTICATION_HTTP_BASIC_USERNAME = self.username
        settings.AUTHENTICATION_HTTP_BASIC_PASSWORD = self.password

    async def given(self) -> tuple[int, int]:
        first = await tables.Account.init(
            model={
                "external_id": encryption.encrypt("first-user"),
                "created": date.now() - datetime.timedelta(days=1),
                "updated": date.now() - datetime.timedelta(days=1),
                "blocked": None,
                "authorization": None,
            }
        )
        second = await tables.Account.init(
            model={
                "external_id": encryption.encrypt("second-user"),
                "created": date.now(),
                "updated": date.now(),
                "blocked": None,
                "authorization": None,
            }
        )

        return first.id, second.id

    async def when(
        self,
        *,
        account_id: int | None = None,
        direction: str = "desc",
        page: int = 1,
        size: int = 10,
        password: str = "password",
    ) -> dict:
        request = await self.client.post(
            "/api/-/accounts:search",
            json={
                "filters": {
                    "id": account_id,
                },
                "sorting": {
                    "direction": direction,
                },
                "pagination": {
                    "page": page,
                    "size": size,
                },
            },
            auth=("admin", password),
        )
        request.raise_for_status()
        return request.json()

    @pytest.mark.asyncio
    async def test_desc(self) -> None:
        first_id, second_id = await self.given()

        response = await self.when(direction="desc")

        assert response["total"] == 2
        assert [item["id"] for item in response["items"]] == [second_id, first_id]
        assert [item["external_id"] for item in response["items"]] == ["second-user", "first-user"]

    @pytest.mark.asyncio
    async def test_asc(self) -> None:
        first_id, second_id = await self.given()

        response = await self.when(direction="asc")

        assert response["total"] == 2
        assert [item["id"] for item in response["items"]] == [first_id, second_id]

    @pytest.mark.asyncio
    async def test_filter_by_id(self) -> None:
        _, second_id = await self.given()

        response = await self.when(account_id=second_id)

        assert response["total"] == 1
        assert [item["id"] for item in response["items"]] == [second_id]

    @pytest.mark.asyncio
    async def test_pagination(self) -> None:
        await self.given()

        response = await self.when(direction="desc", page=2, size=1)

        assert response["total"] == 2
        assert len(response["items"]) == 1
        assert response["items"][0]["external_id"] == "first-user"

    @pytest.mark.asyncio
    async def test_unauthorized(self) -> None:
        request = await self.client.post(
            "/api/-/accounts:search",
            json={
                "filters": {
                    "id": None,
                },
                "sorting": {
                    "direction": "desc",
                },
                "pagination": {
                    "page": 1,
                    "size": 10,
                },
            },
            auth=("admin", fake.password()),
        )

        assert request.status_code == 401
