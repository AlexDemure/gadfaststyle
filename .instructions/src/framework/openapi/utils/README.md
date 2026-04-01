## Описание

`framework/openapi/utils` описывает утилиты OpenAPI-слоя.

## Правила

- Утилиты должны быть переиспользуемыми внутри OpenAPI-каркаса.
- Не смешивай их с handlers и моделями.
- Утилиты не должны зависеть от предметного HTTP-кода.

## Примеры

```python
from src.framework.openapi.utils import specification
```
