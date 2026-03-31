## Описание

`update` описывает сценарии обновления.

## Правила

- Обновляй только поля, которые входят в контракт сценария.
- Проверки конфликтов и недопустимых переходов состояния оставляй в usecase или домене.
- Не вводи новый patch-формат без необходимости, если рядом уже принят другой стиль.
- Если модель использует `__encrypted__`, шифруй изменяемые значения до передачи в repository или через helper модели.
- Если `update` возвращает доменную модель, возвращай ее в дешифрованной форме.

## Примеры

```python
class Usecase:
    @sessionmaker.write
    async def __call__(self, session: Session, account_id: int, external_id: str) -> Account:
        self.build(session)
        await self.validate(account_id=account_id, external_id=external_id)

        account = await self.container.repository.account.update(
            filters={"id": account_id},
            values=Account.encrypt(
                encrypter=self.container.security.encryption.encrypt,
                external_id=external_id,
            ),
        )

        return decrypt(
            decrypter=self.container.security.encryption.decrypt,
            account=account,
        )
```
