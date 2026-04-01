## Описание

`monitoring/asyncio` описывает мониторинг asyncio-runtime.

## Правила

- Здесь держи только технический код наблюдения за event loop.
- Детекторы и handlers раскладывай по подпакетам.
- Monitoring-код не должен содержать бизнесовую логику.

## Примеры

```python
from src.infrastructure.monitoring.asyncio import detector
```
