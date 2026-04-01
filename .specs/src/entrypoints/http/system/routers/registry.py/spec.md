# src/entrypoints/http/system/routers/registry.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Собрать и зарегистрировать элементы пакета `src/entrypoints/http/system/routers`.

## Поведение

Модуль объединяет и регистрирует элементы пакета в одном месте.

## Входы

- Прямые входы определяются вызывающим кодом модуля.

## Выходы

- Результат определяется контрактом вызывающего кода.

## Зависимости

- `src.framework.routing: APIRouter`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
