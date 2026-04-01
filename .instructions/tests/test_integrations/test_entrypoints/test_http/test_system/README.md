## Описание

`test_http/test_system` описывает интеграционные тесты системных HTTP-ручек.

## Правила

- Здесь проверяй system-маршруты и их контур доступа.
- Тесты должны идти через system-router и его зависимости.
- Не смешивай здесь public-сценарии.

## Примеры

```python
request = await self.client.get("/api/system/accounts:get")
```
