## Описание

`logging/mappers` описывает мапперы лог-событий.

## Правила

- Mapper преобразует технические данные в структуру логирования.
- Не смешивай маппинг с formatter- и parser-логикой.
- Mapper не должен содержать бизнесовую интерпретацию событий.

## Примеры

```python
from src.infrastructure.monitoring.logging import mappers
```
