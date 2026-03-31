## Описание

`common` описывает общий HTTP-код.

## Правила

- В `common` храни только код, который используется в нескольких контурах или доменах.
- Общие request, response и pagination-схемы размещай здесь.
- Если код нужен только одному контуру, оставляй его в `public` или `system`.

## Примеры

```python
from src.entrypoints.http.common.schemas import Request
from src.entrypoints.http.common.schemas import Response
```
