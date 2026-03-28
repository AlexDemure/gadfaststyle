# HTTP: System

## Что входит в раздел

- `src/entrypoints/http/system/routers/`
- `src/entrypoints/http/system/deps/`
- `src/entrypoints/http/system/schemas/`

## Назначение

`system` содержит внутренние или административные HTTP-ручки.

## Как организовывать

- Для нового домена создавай отдельные директории:
  - `src/entrypoints/http/system/routers/<domain>/`
  - `src/entrypoints/http/system/deps/<domain>/`
- Схемы домена добавляй в модуль внутри `src/entrypoints/http/system/schemas/`, если это соответствует текущему стилю.
- Детали по `routers` читай в `.ai/architecture/src/http/system/routers/instruction.md`.
- Детали по `deps` и `schemas` читай в:
  - `.ai/architecture/src/http/system/deps/instruction.md`
  - `.ai/architecture/src/http/system/schemas/instruction.md`
- Новый домен обязательно подключай через существующий `registry.py`.
- Если после удаления ручек у домена не остается файлов, удаляй пустые папки домена в `routers/` и `deps/` и чисти верхние `registry.py`.

## Ориентир

Сохраняй ту же форму, что и в `public`, но проверяй ближайшую реализацию внутри `src/entrypoints/http/system/`.
