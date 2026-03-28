# HTTP: Public

## Что входит в раздел

- `src/entrypoints/http/public/routers/`
- `src/entrypoints/http/public/deps/`
- `src/entrypoints/http/public/schemas/`

## Назначение

`public` содержит публичные HTTP-ручки и все связанные с ними схемы и dependency.

## Как организовывать

- Для нового домена создавай отдельные директории:
  - `src/entrypoints/http/public/routers/<domain>/`
  - `src/entrypoints/http/public/deps/<domain>/`
- Схемы домена добавляй в модуль внутри `src/entrypoints/http/public/schemas/`, если это соответствует текущему стилю.
- Детали по `routers` читай в `.ai/architecture/src/http/public/routers/instruction.md`.
- Детали по `deps` и `schemas` читай в:
  - `.ai/architecture/src/http/public/deps/instruction.md`
  - `.ai/architecture/src/http/public/schemas/instruction.md`
- Домен подключай через `registry.py`, иначе ручка не попадет в приложение.
- Если после удаления ручек у домена не остается файлов, удаляй пустые папки домена в `routers/` и `deps/` и чисти верхние `registry.py`.

## Ориентир

Ориентируйся на `src/entrypoints/http/public/routers/accounts/`, `src/entrypoints/http/public/deps/accounts/` и `src/entrypoints/http/public/schemas/accounts.py`.
