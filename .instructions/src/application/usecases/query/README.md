## Описание

`query` описывает usecase чтения.

## Правила

- Используй `@sessionmaker.read`.
- Query-usecase не меняет состояние сущности и не содержит write-операций.
- Для чтения одной сущности используй `get`.
- Для чтения коллекции используй `search`.
- Допускается только минимальная orchestration-логика вокруг чтения.

## Примеры

```python
@sessionmaker.read
async def __call__(self, session: Session, external_id: str) -> Account:
    self.build(session)
```
