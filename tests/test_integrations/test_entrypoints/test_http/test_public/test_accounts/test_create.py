from httpx import AsyncClient

from src.entrypoints.http.public.deps.accounts.create import dependency
from src.infrastructure.security.jwt.models import Tokens

from tests.faker import fake


class FakeUsecase:
    async def __call__(self, external_id: str) -> Tokens:
        assert external_id
        return Tokens(access="access-token", refresh="refresh-token")


async def test_create_account(client: AsyncClient, app) -> None:
    app.dependency_overrides[dependency] = lambda: FakeUsecase()

    response = await client.post("/api/accounts:create", json={"external_id": fake.uuid4()})

    assert response.status_code == 201
    assert response.json() == {
        "access": "access-token",
        "refresh": "refresh-token",
    }
