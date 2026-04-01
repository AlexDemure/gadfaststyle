# src/common/formats/utils/string.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Описать публичное поведение модуля `src/common/formats/utils/string.py`.

## Поведение

Модуль определяет Функции: `strip`, `normalized`, `compact`, `truncate`, `remove`, `empty`, `number`, `count`, `lower`, `upper`, `title`, `capitalize`, `sentence`, `acronym`, `words`, `snake`, `camel`, `pascal`, `kebab`, `split`, `join`, `splitlines`.

## Входы

- `string`
- `clean`
- `length`
- `prefix`
- `suffix`
- `preserve`
- `separator`
- `words`

## Выходы

- `str`
- `bool`
- `int`
- `list[str]`

## Зависимости

- `contextlib`
- `unicodedata`
- `src.common.formats.collections: ENCODING_ASCII`
- `src.common.formats.collections: ENCODING_ERROR_IGNORE`
- `src.common.formats.collections: REGEXP_NON_ALPHANUMERIC`
- `src.common.formats.collections: REGEXP_PASCAL_WORDS`
- `src.common.formats.collections: UNICODE_NORMALIZATION_FORM`
- `src.common.keyboard.collections: SYMBOL_COMMA`
- `src.common.keyboard.collections: SYMBOL_DOT`
- `src.common.keyboard.collections: SYMBOL_EMPTY`
- `src.common.keyboard.collections: SYMBOL_HYPHEN`
- `src.common.keyboard.collections: SYMBOL_LOWER_HYPHEN`
- `src.common.keyboard.collections: SYMBOL_TRUNCATION`
- `src.common.keyboard.collections: SYMBOL_WHITESPACE`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
