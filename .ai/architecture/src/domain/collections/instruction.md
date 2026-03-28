# Domain: Collections

## Что входит в раздел

- `src/domain/collections/exceptions/`
- `src/domain/collections/enums/`

## Назначение

`collections` содержит доменные исключения, enum и другие доменные наборы значений, которые переиспользуются в нескольких местах проекта.

## Правила

- Разделяй типы доменных коллекций по соответствующим подпапкам.
- Ошибки домена описывай в `exceptions/`.
- Enum и наборы допустимых значений описывай в `enums/`.
- Не складывай в `collections` прикладные helper-функции или инфраструктурный код.

## Навигация

- `.ai/architecture/src/domain/collections/exceptions/instruction.md`
- `.ai/architecture/src/domain/collections/enums/instruction.md`
