## Описание

`get` описывает чтение одной сущности или состояния.

## Правила

- `get` возвращает одну сущность или одно состояние.
- Разные способы чтения разделяй по разным файлам внутри `get/`.
- Не смешивай `get` и `search`.
- Если после чтения нужна бизнесовая проверка состояния, делай ее в usecase.
- Если `get` возвращает доменную модель с зашифрованными полями, возвращай ее в дешифрованной форме.

## Примеры

```python
@sessionmaker.read
async def __call__(self, session: Session, external_id: str) -> Account:
    self.build(session)

    account = await self.container.repository.account.one(
        Filter.eq(key="external_id", value=external_id)
    )

    if account.blocked:
        raise AccountBlocked

    return decrypt(
        decrypter=self.container.security.encryption.decrypt,
        account=account,
    )
```
