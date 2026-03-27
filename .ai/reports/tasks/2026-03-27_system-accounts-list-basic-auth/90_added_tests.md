# Added Tests

```python
# path: tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/test_list.py
import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.formats.utils import date
from src.configuration import settings
from src.infrastructure.security.encryption import encryption

from tests.factories.infrastructure.databases.postgres import tables
from tests.faker import fake


class TestAccountsList:
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

    async def given(self) -> None:
        for external_id in ["first-user", "second-user"]:
            await tables.Account.init(
                model={
                    "external_id": encryption.encrypt(external_id),
                    "created": date.now(),
                    "updated": date.now(),
                    "blocked": None,
                    "authorization": None,
                }
            )

    async def when(self) -> dict:
        request = await self.client.get(
            "/api/-/accounts",
            params={
                "page": 1,
                "size": 10,
            },
            auth=("admin", "password"),
        )
        request.raise_for_status()

        return request.json()

    async def then(self, response: dict) -> None:
        assert response["total"] == 2
        assert {item["external_id"] for item in response["items"]} == {"first-user", "second-user"}
        assert all(isinstance(item["id"], int) for item in response["items"])

    @pytest.mark.asyncio
    async def test(self) -> None:
        await self.given()
        response = await self.when()
        await self.then(response)

    @pytest.mark.asyncio
    async def test_unauthorized(self) -> None:
        request = await self.client.get(
            "/api/-/accounts",
            params={
                "page": 1,
                "size": 10,
            },
            auth=("admin", fake.password()),
        )

        assert request.status_code == 401
```
