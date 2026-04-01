# src/common/formats/collections/__init__.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:34:57

## Назначение

Собрать публичный экспорт пакета `collections`.

## Поведение

Файл собирает и экспортирует: `ENCODING_ASCII`, `ENCODING_ERROR_IGNORE`, `ENCODING_UTF`, `Format`, `REGEXP_NON_ALPHANUMERIC`, `REGEXP_PASCAL_WORDS`, `UNICODE_NORMALIZATION_FORM`.

## Входы

- Импортируемые объекты пакета: `ENCODING_ASCII`, `ENCODING_ERROR_IGNORE`, `ENCODING_UTF`, `Format`, `REGEXP_NON_ALPHANUMERIC`, `REGEXP_PASCAL_WORDS`, `UNICODE_NORMALIZATION_FORM`

## Выходы

- Публичный импорт `ENCODING_ASCII`
- Публичный импорт `ENCODING_ERROR_IGNORE`
- Публичный импорт `ENCODING_UTF`
- Публичный импорт `Format`
- Публичный импорт `REGEXP_NON_ALPHANUMERIC`
- Публичный импорт `REGEXP_PASCAL_WORDS`
- Публичный импорт `UNICODE_NORMALIZATION_FORM`

## Зависимости

- `const: ENCODING_ASCII`
- `const: ENCODING_ERROR_IGNORE`
- `const: ENCODING_UTF`
- `const: REGEXP_NON_ALPHANUMERIC`
- `const: REGEXP_PASCAL_WORDS`
- `const: UNICODE_NORMALIZATION_FORM`
- `enums: Format`

## Ограничения

- Файл должен оставаться в границах своего слоя и каталога.
- Файл не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
- Файл не должен содержать бизнес-логику вне публичного экспорта пакета.
