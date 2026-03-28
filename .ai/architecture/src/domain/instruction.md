# Architecture: Domain Layer

## Назначение

Эта папка зеркалит `src/domain/` и служит входной точкой для инструкций domain-слоя.

Сейчас основной фокус domain-слоя в проекте:

- `src/domain/models/`
- `src/domain/collections/`

## Порядок чтения

1. Прочитай этот файл.
2. Если задача меняет доменную сущность, открой `.ai/architecture/src/domain/models/instruction.md`.
3. Если задача меняет доменные коллекции, открой `.ai/architecture/src/domain/collections/instruction.md`.
4. Если задача касается ошибок домена, продолжи в `.ai/architecture/src/domain/collections/exceptions/instruction.md`.
5. Если задача касается enum или других доменных констант, продолжи в `.ai/architecture/src/domain/collections/enums/instruction.md`.
6. Только потом читай ближайший реальный модуль в `src/domain/`.

## Что важно

- Domain не должен знать про HTTP-слой, БД-таблицы и прочие инфраструктурные детали.
- Новый код в domain должен зеркалить существующую структуру `src/domain/`.
- Если в домене уже принят конкретный паттерн, например `Base`, `init(...)` или `__encrypted__`, повторяй его.
