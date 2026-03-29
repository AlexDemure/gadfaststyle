## Правила

- Infrastructure изолирует внешние системы и технические реализации.
- Форму infrastructure-пакетов задают инструкции этой папки.
- Lifecycle, singleton setup и конфигурация должны оставаться явными.
- Размещай новые пакеты по типу интеграции.
- Database runtime и database clients размещай в `databases/`.
- Внешние API и сервисные интеграции размещай в `integrations/`.
- Security-клиенты размещай в `security/`.
- Storage-клиенты размещай в `storages/`.
- Monitoring-пакеты размещай в `monitoring/`.
- Новый инфраструктурный клиент оформляй как singleton.
- Singleton собирай через `setup.py` и экспортируй через `__init__.py`.
- Если клиент управляет жизненным циклом, добавляй методы `start()` и `shutdown()`.
- Lifecycle клиента подключай в `src/bootstrap/server.py`.
- Конфигурацию клиента добавляй в `src/configuration/setup.py` отдельным классом `BaseSettings`.
- Новый класс конфигурации добавляй в список `configs`.
- Новые переменные конфигурации добавляй в `.env` и `.env.example`.
