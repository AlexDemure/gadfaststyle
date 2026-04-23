# Quick Rules

- Тестируем endpoint-ы через HTTP.
- Usecase не подменяем.
- `setup` готовит данные через фабрики и БД.
- В `setup` нет HTTP-запросов.
- Redis мокается явно в `test(...)`.
- Мокаются только те методы Redis, которые реально участвуют в сценарии.
- Один класс = один сценарий.

# Структура

```text
tests/
├── factories/
├── mocking/
├── test_integrations/
└── tools/
```

# Базовые зависимости

Используй:

```python
from tests.faker import fake
from tests.factories.infrastructure.databases.postgres.tables import Account
from tests.mocking.infrastructure.storages.redis.client import Redis
```

# Фикстуры

`tests/test_integrations/conftest.py` даёт:

- `app`
- `client`
- `session`

`session` — transactional `AsyncSession`:
- данные видны endpoint-ам без `commit`;
- все изменения откатываются после теста;
- фабрики получают session через `table._meta.sqlalchemy_session`.

# Сценарий

Шаблон:

```python
class TestGetCurrentAccount:
    client: AsyncClient
    session: AsyncSession

    async def setup(self) -> None: ...

    async def process(self) -> Response: ...

    async def check(self, response: Response) -> None: ...

    async def test(
        self,
        client: AsyncClient,
        session: AsyncSession,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        self.client = client
        self.session = session

        await self.setup()

        response = await self.process()

        await self.check(response)
```

# Правила сценария

- `setup` только готовит данные и контекст.
- `process` делает один целевой HTTP-запрос.
- `process` возвращает `Response`.
- `check` проверяет HTTP-ответ и состояние БД.
- `check` принимает `response` аргументом.
- Если нужен cache mock, patch делай в `test(...)`.
- Для вариантов используй `@pytest.mark.parametrize` на `test(...)`.

# Что проверяется

- HTTP contract endpoint-а;
- прикладной сценарий usecase;
- взаимодействие с БД;
- transport-layer wiring без подмены usecase.

# Окружение

Для интеграционных тестов нужны:

- Postgres
- `POSTGRES` в `.env`
- `JWT` в `.env`
- `CRYPTOGRAPHY` в `.env`
