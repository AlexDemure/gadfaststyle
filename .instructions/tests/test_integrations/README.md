## Описание

`test_integrations` описывает интеграционные тесты.

## Правила

- В первую очередь покрывай HTTP-сценарии интеграционными тестами.
- Тесты размещай в зеркальной структуре относительно production-кода.
- Для HTTP используй `httpx.AsyncClient`.
- Для доступа к БД используй `AsyncSession` и существующие фикстуры.
- Тест оформляй в стиле `given / when / then`, если это не ухудшает читаемость.

## Примеры

```python
class TestAccountCreate:
    async def given(self) -> None: ...

    async def when(self) -> Tokens:
        request = await self.client.post("/api/accounts:create", json={"external_id": fake.uuid4()})
        request.raise_for_status()
        return Tokens.model_validate(request.json())

    async def then(self) -> None: ...
```
