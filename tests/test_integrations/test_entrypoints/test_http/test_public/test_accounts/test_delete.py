from httpx import AsyncClient

from src.entrypoints.http.public.deps.accounts.delete import dependency


class FakeUsecase:
    async def __call__(self, token: str) -> None:
        assert token == "access-token"


async def test_delete_current_account(client: AsyncClient, app) -> None:
    app.dependency_overrides[dependency] = lambda: FakeUsecase()

    response = await client.delete(
        "/api/accounts:current",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 204


async def test_delete_current_account_unauthorized(client: AsyncClient) -> None:
    response = await client.delete("/api/accounts:current")

    assert response.status_code == 401
