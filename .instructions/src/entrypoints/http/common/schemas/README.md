## Описание

`schemas` описывает общие HTTP-схемы.

## Правила

- Общие request, response и pagination-схемы размещай в `common/schemas`.
- Публичные схемы экспортируй через `schemas/__init__.py`.
- Из контуров импортируй схемы через пакет, если экспорт уже собран.

## Примеры

```python
from src.entrypoints.http.common.schemas import Pagination
from src.entrypoints.http.common.schemas import Response
```
