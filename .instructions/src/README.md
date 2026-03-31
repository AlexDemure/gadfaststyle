## Описание

`src` описывает production-код проекта.

## Правила

- Соблюдай слои: `entrypoints -> application -> domain`, `infrastructure` подключается снизу и не тянется в `domain`.
- Импорты группируй блоками: стандартная библиотека, сторонние пакеты, импорты проекта.
- Между группами импортов оставляй одну пустую строку.
- Между верхнеуровневыми классами и функциями оставляй одну пустую строку.
- Если пакет уже собирает публичные объекты через `__init__.py`, импортируй из пакета, а не из внутренних файлов.
- Текущий базовый каркас `src/` зафиксирован ниже и повторен в `.templates/project.toml`.
- В `.templates/project.toml` храни только скелет слоев и tooling-пакетов без доменных ручек, таблиц и предметных модулей.

## Примеры

```text
src/
├── application/
│   ├── usecases/
│   └── utils/
├── bootstrap/
├── common/
│   ├── formats/
│   ├── http/
│   ├── keyboard/
│   ├── os/
│   └── typings/
├── configuration/
├── decorators/
├── domain/
│   ├── collections/
│   └── models/
├── entrypoints/
│   └── http/
│       ├── common/
│       ├── public/
│       └── system/
├── framework/
│   ├── background/
│   ├── collections/
│   ├── openapi/
│   └── routing/
├── infrastructure/
│   ├── databases/
│   │   ├── orm/
│   │   └── postgres/
│   ├── monitoring/
│   ├── security/
│   └── storages/
└── static/
```

```python
from src.domain.collections import AccountNotFound
from src.domain.models import Account
from src.infrastructure.databases.postgres import adapters
```
