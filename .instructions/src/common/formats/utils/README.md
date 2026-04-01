## Описание

`formats/utils` описывает утилиты работы с форматами и преобразованиями.

## Правила

- Каждая утилита решает одну техническую задачу.
- Утилиты не зависят от `application`, `domain` и `entrypoints`.
- Если утилита становится domain-specific, вынеси ее из `common`.

## Примеры

```python
from src.common.formats.utils import date
from src.common.formats.utils import uuid
```
