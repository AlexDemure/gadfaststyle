# Architecture: HTTP Layer

## Назначение

Эта папка зеркалит `src/entrypoints/http/` и служит входной точкой для инструкций HTTP-слоя.

Сейчас основной фокус HTTP-слоя в проекте:

- `src/entrypoints/http/common/`
- `src/entrypoints/http/public/`
- `src/entrypoints/http/system/`

## Порядок чтения

1. Прочитай этот файл.
2. Определи, какой HTTP-контур затрагивает задача:
   - `.ai/architecture/src/http/public/instruction.md`
   - `.ai/architecture/src/http/system/instruction.md`
   - `.ai/architecture/src/http/common/instruction.md`
3. Если задача меняет endpoint-слой, продолжи чтение по дереву:
   - `.ai/architecture/src/http/public/routers/instruction.md` или `.ai/architecture/src/http/system/routers/instruction.md`
   - `.ai/architecture/src/http/public/deps/instruction.md` или `.ai/architecture/src/http/system/deps/instruction.md`
   - `.ai/architecture/src/http/public/schemas/instruction.md` или `.ai/architecture/src/http/system/schemas/instruction.md`
4. Для конкретной ручки открой instruction по операции внутри нужного контура:
   - `.ai/architecture/src/http/public/routers/operations/`
   - `.ai/architecture/src/http/system/routers/operations/`
5. Только потом читай ближайший реальный модуль в `src/entrypoints/http/`.

## Что важно

- Новый код должен зеркалить существующую структуру `src/entrypoints/http/`.
- Для нового домена создавай отдельные папки домена в нужном контуре, а не смешивай `public` и `system`.
- Если задача связана с выборками, используй паттерн `search`, а не `list`.
