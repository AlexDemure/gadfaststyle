## Описание

`monitoring/health` описывает health-check инфраструктуру.

## Правила

- Health-check код должен описывать только техническую готовность сервиса.
- Проверки делай легкими и безопасными для runtime.
- Не размещай здесь бизнесовые сценарии.

## Примеры

```python
from src.infrastructure.monitoring import health
```
