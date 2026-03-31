## Описание

`enums` описывает доменные enum.

## Правила

- Enum размещай по смыслу домена.
- Добавляй enum только для ограниченного и стабильного набора значений.
- Не меняй публичную форму enum без необходимости, если он уже используется в других слоях.
- Публичные enum экспортируй через `enums/__init__.py` и `collections/__init__.py`.

## Примеры

```python
from enum import StrEnum


class AccountStatus(StrEnum):
    active = "active"
    blocked = "blocked"
```
