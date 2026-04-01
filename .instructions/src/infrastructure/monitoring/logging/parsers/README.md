## Описание

`logging/parsers` описывает парсеры логов.

## Правила

- Каждый parser отвечает за один формат входных данных.
- Парсинг не должен включать форматирование и отправку логов.
- Ошибки парсинга держи в logging-слое.

## Примеры

```python
from src.infrastructure.monitoring.logging import parsers
```
