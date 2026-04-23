from httpx import AsyncClient
from httpx import Response

from src.infrastructure.security.jwt.models import Tokens

from tests.faker import fake


class TestCreateAccount:
    client: AsyncClient

    async def setup(self) -> None: ...

    async def process(self) -> Response:
        return await self.client.post("/api/accounts:create", json={"external_id": fake.uuid4()})

    @classmethod
    async def check(cls, response: Response) -> None:
        assert response.status_code == 201

        tokens = Tokens.model_validate(response.json())

        assert tokens.access
        assert tokens.refresh

    async def test(self, client: AsyncClient) -> None:
        self.client = client

        await self.setup()

        response = await self.process()

        await self.check(response)
