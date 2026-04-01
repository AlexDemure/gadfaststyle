# src/infrastructure/storages/redis/client.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Реализовать клиент и публичный API модуля `src/infrastructure/storages/redis`.

## Поведение

Модуль реализует клиент, его жизненный цикл и публичные операции слоя.

## Входы

- Параметры конструкторов и публичных методов классов модуля.

## Выходы

- Публичные классы и объекты модуля.

## Зависимости

- `datetime`
- `functools`
- `typing`
- `redis.asyncio`
- `src.common.formats.utils: hashes`
- `src.common.formats.utils: json`
- `src.common.keyboard.collections: SYMBOL_ASTERISK`
- `src.configuration: settings`
- `src.framework.routing: APIRouter`
- `.collections: ClientDisabled`
- `.collections: Namespace`
- `.collections: Operation`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
