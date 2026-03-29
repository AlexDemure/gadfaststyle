## Правила

- `entrypoints` описывает модули подключения разных способов входа в приложение.
- Новые entrypoints размещай по типу входа: `http`, `cron`, `workers`, `services`, `websockets`.
- Каждый entrypoint изолирует свой транспорт или механизм запуска от application-слоя.

