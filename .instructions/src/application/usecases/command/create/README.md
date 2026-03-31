## Описание

`create` описывает сценарии создания.

## Правила

- Для конфликта существования используй ошибку вида `{Model}AlreadyExists`.
- Создавай доменную модель через `Model.init(...)` или уже принятый factory-паттерн.
- Если модель использует `__encrypted__`, шифруй значения до записи или через helper модели.
- Если `create` возвращает доменную модель с зашифрованными полями, возвращай ее в дешифрованной форме.
- Если у модели уже есть `encrypt(...)`, `decrypt(...)` или `normalize(...)`, используй их, а не дублируй логику в usecase.

## Примеры

```python
class Usecase:
    @sessionmaker.write
    async def __call__(self, session: Session, external_id: str) -> Tokens:
        self.build(session)
        await self.validate(external_id=external_id)

        account = await self.container.repository.account.create(
            model=Account.init(
                **Account.encrypt(
                    encrypter=self.container.security.encryption.encrypt,
                    external_id=external_id,
                ),
            )
        )

        return self.container.security.jwt.encode(subject=str(account.id))
```
