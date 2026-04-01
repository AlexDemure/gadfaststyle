## Описание

`entrypoints/http/common/deps` описывает общие HTTP-зависимости.

## Правила

- В `deps` держи только транспортного уровня зависимости для router-слоя.
- Зависимости должны собирать уже готовые объекты, а не содержать бизнесовую логику.
- Общие security и context-deps раскладывай по подпакетам.

## Примеры

```python
from src.entrypoints.http.common.deps import security
```
