# src/infrastructure/security/jwt/client.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Реализовать клиент и публичный API модуля `src/infrastructure/security/jwt`.

## Поведение

Модуль реализует клиент, его жизненный цикл и публичные операции слоя.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `jwt`
- `src.common.formats.utils: date`
- `src.common.formats.utils: uuid`
- `src.configuration: settings`
- `.collections: ClientDisabled`
- `.collections: TokenInvalid`
- `.collections: TokenPurpose`
- `.models: Token`
- `.models: Tokens`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
