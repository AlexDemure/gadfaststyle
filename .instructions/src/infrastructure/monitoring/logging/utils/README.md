## Описание

`logging/utils` описывает утилиты logging-слоя.

## Правила

- Утилиты должны быть техническими и переиспользуемыми.
- Не смешивай их с formatter-, parser- и mapper-реализациями.
- Побочные эффекты делай явными.

## Примеры

```python
from src.infrastructure.monitoring.logging import utils
```
