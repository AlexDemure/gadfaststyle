## Описание

`utils` описывает переиспользуемые прикладные утилиты.

## Правила

- Храни в `utils` только прикладные утилиты с явным переиспользованием.
- Группируй утилиты по домену, а не по типу функции.
- Если логика нужна одному usecase, оставляй ее в самом usecase.
- Не выноси сюда HTTP-логику, SQLAlchemy statement и логику, которая должна жить в `domain` или `infrastructure`.

## Примеры

```python
import typing

from src.domain.models import Account


def decrypt(decrypter: typing.Callable[..., typing.Any], account: Account) -> Account:
    for key, value in Account.decrypt(
        decrypter=decrypter,
        external_id=account.external_id,
    ).items():
        setattr(account, key, value)

    return account
```
