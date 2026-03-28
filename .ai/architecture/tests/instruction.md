# Architecture: Tests

## Что покрываем

- В первую очередь покрываем HTTP-сценарии.
- Основной фокус: интеграционные тесты для публичных ручек.
- Для новых endpoint-ов создаем тесты в зеркальной структуре относительно `src/entrypoints/http/public/`.

## Где писать тесты

Пример расположения:

- `src/entrypoints/http/public/routers/accounts/create.py`
- `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_create.py`

Если появляется новый домен, создавай новую папку `test_<domain>`.
Если после удаления функциональности в тестовом домене не остается тестов, удаляй и пустую папку `test_<domain>`.

## Как писать тест

- Используй `pytest`.
- Используй `httpx.AsyncClient` и `AsyncSession`.
- Используй существующие фикстуры из `tests/test_integrations/conftest.py`.
- Используй `tests.faker.fake` и фабрики из `tests/factories/`, если нужны данные.
- Тест оформляй в стиле `given / when / then`.

Эталон:

```python
# path: tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_create.py
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

## Правила написания

- Не писать новый формат тестов, если сценарий можно выразить через `given / when / then`.
- Для HTTP используем интеграционный тест, а не мокнутый unit-тест endpoint-а.
- Фабрики используем там, где нужно подготовить БД-состояние или связанные сущности.
- Если проверяется ошибка, добавляй отдельный сценарий рядом, а не усложняй один тест.
- Если удаляется endpoint или сценарий, удаляй и его зеркальные тесты, а затем чисти пустые тестовые папки.

## Что не делать

- Не покрывать внутреннюю реализацию usecase отдельно, если задача требует только HTTP-поведение.
- Не дублировать уже существующий happy path без новой проверки.
- Не писать тестовые данные вручную, если подходящая фабрика уже существует.
