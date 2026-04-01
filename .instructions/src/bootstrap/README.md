## Описание

`bootstrap` описывает запуск и сборку рантайма приложения.

## Правила

- В `bootstrap` собирай приложение, lifecycle и стартовые точки входа.
- Здесь допускается связывать `configuration`, `framework`, `entrypoints` и инфраструктурные setup-модули.
- В `bootstrap` не размещай бизнесовую логику, domain-модели и usecase-реализацию.
- Код запуска держи коротким и своди к вызову уже подготовленных setup-функций.

## Примеры

```python
from src.bootstrap.server import server
```
