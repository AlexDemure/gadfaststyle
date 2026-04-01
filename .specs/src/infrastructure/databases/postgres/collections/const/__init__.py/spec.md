# src/infrastructure/databases/postgres/collections/const/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `const`.

## Поведение

Файл собирает и экспортирует: `LENGTH_LARGE_STR`, `LENGTH_MIDDLE_STR`, `LENGTH_PK_STR`, `LENGTH_SMALL_STR`, `LENGTH_TEXT`.

## Входы

- Импортируемые объекты пакета: `LENGTH_LARGE_STR`, `LENGTH_MIDDLE_STR`, `LENGTH_PK_STR`, `LENGTH_SMALL_STR`, `LENGTH_TEXT`

## Выходы

- Публичный импорт `LENGTH_LARGE_STR`
- Публичный импорт `LENGTH_MIDDLE_STR`
- Публичный импорт `LENGTH_PK_STR`
- Публичный импорт `LENGTH_SMALL_STR`
- Публичный импорт `LENGTH_TEXT`

## Зависимости

- `column: LENGTH_LARGE_STR`
- `column: LENGTH_MIDDLE_STR`
- `column: LENGTH_PK_STR`
- `column: LENGTH_SMALL_STR`
- `column: LENGTH_TEXT`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
