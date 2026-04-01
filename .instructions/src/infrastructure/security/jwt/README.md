## Описание

`security/jwt` описывает JWT-инфраструктуру проекта.

## Правила

- В `jwt` держи только техническую работу с токенами.
- Collections и models раскладывай по подпакетам.
- JWT-слой не должен содержать бизнесовые usecase.

## Примеры

```python
from src.infrastructure.security import jwt
```
