## Описание

`tools/profiler/models/profilers/extensions` описывает расширения моделей профилировщиков.

## Правила

- Расширения должны оставаться техническими и изолированными.
- Не добавляй сюда runtime-логику запуска.
- Каждое расширение решает одну задачу модели.

## Примеры

```python
from tests.tools.profiler.models.profilers import extensions
```
