## Описание

`specs` описывает формат `spec.md` для отдельных участков проекта.

## Правила

- `.specs` повторяет структуру `src` и `tests`.
- Каждый `spec.md` относится только к одному участку проекта и одному направлению.
- Для backend используй `.specs/src/<path-to-file>/spec.md`.
- Для tests используй `.specs/tests/<path-to-file>/spec.md`.
- Путь `src/infrastructure/databases/postgres/migrations/` не документируется в `.specs/`.
- Каждый `spec.md` начинается с блока `Статус`.
- В `Статус` храни поля `created_at`, `system_analyst_updated_at`, `team_lead_synced_at`, `backend_synced_at`, `tester_synced_at`, `spec_sync_synced_at`.
- Все поля времени записывай в формате `YYYY-MM-DD HH:MM:SS`.
- После `Статус` описывай только поведение текущего участка проекта.
- Не смешивай backend, tests и будущий frontend в одном `spec.md`.
- Пиши техническое поведение без кода и без вариантов решения.

## Примеры

```md
# .specs/src/application/usecases/accounts/update.py/spec.md

## Статус

- created_at: 2026-03-31 12:30:00
- system_analyst_updated_at: 2026-03-31 12:30:00
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: null

## Назначение

Обновить аккаунт текущего пользователя.

## Поведение

Usecase принимает изменяемые поля аккаунта, валидирует их и сохраняет новое состояние.

## Входы

- `account_id`
- `external_id`

## Выходы

- Обновленная доменная модель аккаунта.

## Зависимости

- Repository adapter аккаунтов.
- Security-утилиты для шифрования полей.

## Ограничения

- Обновляются только поля из контракта сценария.
- Конфликты проверяются до записи.
```

```md
# .specs/tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_update.py/spec.md

## Статус

- created_at: 2026-03-31 12:30:00
- system_analyst_updated_at: 2026-03-31 12:30:00
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: null

## Назначение

Проверить HTTP-сценарий обновления аккаунта.

## Поведение

Интеграционный тест отправляет запрос на обновление аккаунта и проверяет успешный ответ и сохранение данных.

## Входы

- Тестовый клиент.
- Тестовый аккаунт.

## Выходы

- Подтверждение обновления через HTTP и persistence-слой.

## Зависимости

- `AsyncClient`
- Тестовые фабрики

## Ограничения

- Тест работает через публичный HTTP-контур.
```
