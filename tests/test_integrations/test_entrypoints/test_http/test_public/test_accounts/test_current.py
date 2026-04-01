from httpx import AsyncClient

from src.domain.models import Account
from src.entrypoints.http.public.deps.accounts.current import dependency
from src.entrypoints.http.public.schemas import CurrentAccount


class FakeUsecase:
    async def __call__(self, token: str) -> Account:
        assert token == "access-token"
        return Account(
            id=1,
            external_id="external-id",
            created="2026-04-01T12:00:00+00:00",
            updated="2026-04-01T12:00:00+00:00",
        )


async def test_get_current_account(client: AsyncClient, app) -> None:
    app.dependency_overrides[dependency] = lambda: FakeUsecase()

    response = await client.get(
        "/api/accounts:current",
        headers={"Authorization": "Bearer access-token"},
    )

    assert response.status_code == 200
    assert response.json() == CurrentAccount.serialize(
        Account(
            id=1,
            external_id="external-id",
            created="2026-04-01T12:00:00+00:00",
            updated="2026-04-01T12:00:00+00:00",
        )
    ).model_dump(mode="json")


async def test_get_current_account_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/api/accounts:current")

    assert response.status_code == 403
