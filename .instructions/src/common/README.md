## Описание

`common` описывает общие утилиты и типы проекта.

## Правила

- В `common` держи только переиспользуемый код без бизнесовой логики.
- Утилиты форматов, HTTP, OS, keyboard и typing раскладывай по своим подпакетам.
- `common` не импортирует `application`, `entrypoints`, `domain` и предметную инфраструктуру.
- Если пакет уже собирает публичные объекты через `__init__.py`, импортируй из пакета.

## Примеры

```python
from src.common.formats.utils import date
from src.common.typings.validators import string
```
