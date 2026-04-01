## Описание

`formats/collections/enums` описывает enum слоя форматов.

## Правила

- Используй enum только для ограниченных наборов значений.
- Значения enum должны быть стабильными и не зависеть от runtime.
- Не размещай здесь вспомогательные функции.

## Примеры

```python
import enum


class Mode(str, enum.Enum):
    JSON = "json"
```
