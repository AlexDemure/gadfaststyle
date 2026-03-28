# Infrastructure: Security

## Что входит в раздел

- `src/infrastructure/security/encryption/`
- `src/infrastructure/security/jwt/`

## Назначение

`security` содержит инфраструктурные клиенты и модели для шифрования, токенов и другой security-логики.

## Базовые правила

- Новый security-клиент должен повторять текущий паттерн `client.py`, `setup.py`, `__init__.py`.
- Если клиент управляет внешним соединением или состоянием, он должен иметь lifecycle-методы `start()` и `shutdown()`.
- Конфигурация клиента должна читаться из `settings`, а не из произвольных `os.getenv`.
- Публичный singleton экспортируй так же, как это уже сделано рядом.

## Ориентир

Смотри `src/infrastructure/security/encryption/` и `src/infrastructure/security/jwt/`.
