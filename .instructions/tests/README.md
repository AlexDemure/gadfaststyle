## Описание

`tests` описывает тестовый слой.

## Правила

- Тесты размещай в зеркальной структуре относительно production-кода.
- Используй `pytest`.
- Если нужны данные, сначала используй `tests.faker.fake` и фабрики из `tests/factories/`.
- Не дублируй вручную тестовые данные, если рядом уже есть подходящая фабрика.
- Текущий базовый каркас `tests/` зафиксирован ниже и повторен в `.templates/project.toml`.
- В `.templates/project.toml` храни только тестовый скелет и инструменты без доменных тест-кейсов.

## Примеры

```text
tests/
├── factories/
│   ├── domain/
│   └── infrastructure/
├── mocking/
│   └── infrastructure/
├── test_integrations/
│   └── test_entrypoints/
│       └── test_http/
│           ├── test_public/
│           └── test_system/
├── test_loads/
├── test_units/
└── tools/
    └── profiler/
        ├── contextmanagers/
        ├── models/
        ├── profilers/
        └── reports/
```

```python
from tests.faker import fake
from tests.factories.domain.models import Account
from tests.mocking.infrastructure.storages.redis import Redis
```
