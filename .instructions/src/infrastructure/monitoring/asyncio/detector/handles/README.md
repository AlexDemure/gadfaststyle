## Описание

`monitoring/asyncio/detector/handles` описывает handlers asyncio-detector.

## Правила

- Каждый handler обрабатывает один тип детектора или одно действие.
- Не смешивай здесь сбор сигнала и его логирование.
- Handler должен быть техническим и переиспользуемым.

## Примеры

```python
from src.infrastructure.monitoring.asyncio.detector import handles
```
