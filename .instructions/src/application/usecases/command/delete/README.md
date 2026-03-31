## Описание

`delete` описывает сценарии удаления.

## Правила

- Если нужно проверить существование или допустимость удаления, используй `validate(...)`.
- Не раздувай `delete` лишней логикой, если сценарий сводится к вызову repository.
- Если удаление мягкое, usecase не должен знать детали persistence-реализации.
- Возвращай `None`, если контракт сценария не требует тела ответа.

## Примеры

```python
class Usecase:
    @sessionmaker.write
    async def __call__(self, session: Session, account_id: int) -> None:
        self.build(session)
        await self.container.repository.account.delete(
            Filter.eq(key="id", value=account_id)
        )
```
