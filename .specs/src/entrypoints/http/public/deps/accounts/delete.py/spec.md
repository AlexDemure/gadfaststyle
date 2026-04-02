# src/entrypoints/http/public/deps/accounts/delete.py

## Статус

- created_at: 2026-04-02 10:00:00
- system_analyst_updated_at: 2026-04-02 10:00:00
- team_lead_synced_at: 2026-04-02 10:30:00
- backend_synced_at: 2026-04-02 10:30:00
- tester_synced_at: 2026-04-02 10:30:00
- spec_sync_synced_at: null

## Назначение

Поднять dependency для usecase удаления текущего аккаунта.

## Поведение

Dependency создаёт экземпляр `Usecase` для ручки удаления текущего аккаунта и возвращает его вызывающей стороне.

## Входы

- Нет внешних входов.

## Выходы

- Экземпляр `Usecase`

## Зависимости

- `src.application.usecases.accounts.delete: Usecase`

## Ограничения

- Dependency не должен содержать бизнес-логику и инфраструктурные детали вне сборки usecase.
