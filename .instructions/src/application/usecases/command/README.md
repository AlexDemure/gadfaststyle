## Описание

`command` описывает usecase записи.

## Правила

- Используй `@sessionmaker.write`.
- Предварительные проверки выноси в `validate(...)`.
- `validate(...)` принимает только данные для проверки и ничего не возвращает.
- Проверки конфликтов, существования и переходов состояния выполняй до mutation-операции.
- Mutation-usecase держит orchestration: проверки, security, нормализацию входа и вызовы repository.

## Примеры

```python
@sessionmaker.write
async def __call__(self, session: Session, account_id: int) -> None:
    self.build(session)
    await self.validate(account_id=account_id)
```
