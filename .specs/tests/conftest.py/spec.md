# tests/conftest.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Собрать общие фикстуры и настройку тестового пакета `tests`.

## Поведение

Модуль определяет общие фикстуры и подготовку окружения для тестового пакета.

## Входы

- Прямые входы определяются вызывающим кодом модуля.

## Выходы

- `typing.Generator[asyncio.AbstractEventLoop, None, None]`

## Зависимости

- `asyncio`
- `typing`
- `pytest`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен переносить production-логику в тестовый слой.
