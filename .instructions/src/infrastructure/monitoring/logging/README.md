## Описание

`monitoring/logging` описывает logging-инфраструктуру проекта.

## Правила

- В `logging` держи только логирование, форматирование и парсинг логов.
- Collections, formatters, mappers, models, parsers и utils раскладывай по подпакетам.
- Logging-код не должен содержать бизнесовую логику.

## Примеры

```python
from src.infrastructure.monitoring.logging import formatters
```
