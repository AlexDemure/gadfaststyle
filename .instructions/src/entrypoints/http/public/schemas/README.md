## Описание

`schemas` описывает public HTTP-схемы.

## Правила

- Схемы одного домена группируй в одном модуле, если пакет уже следует этой форме.
- Для request используй базовые классы из `http/common`.
- Для response используй `Response`.
- Имена схем строй как `<Operation><Entity>`.
- Для `search` используй явную структуру `filters`, `sorting`, `pagination`.
- Публичные схемы экспортируй через `schemas/__init__.py`, чтобы код писал `from ...schemas import CurrentAccount`.

## Примеры

```python
class CreateAccount(Public, Request, Command):
    external_id: str


class CurrentAccount(Public, Response):
    id: int

    @classmethod
    def serialize(cls, account: Account) -> typing.Self:
        return cls(id=field.required(account.id))
```
