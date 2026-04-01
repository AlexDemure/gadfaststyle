## Описание

`monitoring/asyncio/detector` описывает детекторы проблем asyncio-runtime.

## Правила

- Каждый detector отвечает за один тип сигнала или события.
- Detector не должен напрямую заниматься форматированием логов.
- Технические handlers выноси в `handles/`.

## Примеры

```python
from src.infrastructure.monitoring.asyncio.detector import handles
```
