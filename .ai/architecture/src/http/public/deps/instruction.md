# HTTP Public: Dependencies

## Что входит в раздел

- `src/entrypoints/http/public/deps/`

## Правила

- DI-функция лежит рядом с доменом и операцией внутри `public`.
- Называй фабрику `dependency`.
- Никакой сложной логики внутри dependency не нужно, если достаточно вернуть `Usecase()`.
- Если домен уже использует более сложную сборку зависимостей, повторяй текущий паттерн, не вводя новый.

## Эталон

```python
from src.application.usecases.accounts.create import Usecase


def dependency() -> Usecase:
    return Usecase()
```
