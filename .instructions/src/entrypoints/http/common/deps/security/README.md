## Описание

`entrypoints/http/common/deps/security` описывает общие security-зависимости HTTP-слоя.

## Правила

- Здесь держи только транспортного уровня security deps.
- Security deps должны возвращать уже валидированные объекты или контекст запроса.
- Не размещай здесь usecase-логику и доступ к persistence-слою.

## Примеры

```python
from src.entrypoints.http.common.deps import security
```
