## Описание

`logging/formatters` описывает форматтеры логов.

## Правила

- Каждый formatter отвечает за один формат вывода.
- Formatter не должен собирать лог-события и не должен отправлять их наружу.
- Форматирование делай детерминированным.

## Примеры

```python
from src.infrastructure.monitoring.logging import formatters
```
