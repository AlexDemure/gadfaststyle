## Эталонная форма

```python
import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.security.jwt.models import Tokens

from tests.faker import fake


class TestAccountCreate:
    @pytest.fixture(autouse=True)
    async def setup(self, client: AsyncClient, session: AsyncSession) -> None:
        self.client = client
        self.session = session

    async def given(self) -> None: ...

    async def when(self) -> Tokens:
        request = await self.client.post(
            "/api/accounts:create",
            json={
                "external_id": fake.uuid4(),
            },
        )
        request.raise_for_status()

        tokens = Tokens.model_validate(request.json())

        return tokens

    async def then(self) -> None: ...

    @pytest.mark.asyncio
    async def test(self) -> None:
        await self.given()
        await self.when()
        await self.then()
```

