# HTTP: Common

## Что входит в раздел

- `src/entrypoints/http/common/schemas/`
- `src/entrypoints/http/common/deps/`
- `src/entrypoints/http/common/collections/`

## Назначение

`common` содержит общие HTTP-схемы, dependency и коллекции, которые переиспользуются между `public` и `system`.

## Правила

- Выноси сюда только реально общий HTTP-код.
- Не складывай в `common` код одного домена, если он не переиспользуется между контурами.
- Базовые request/response/pagination-схемы должны жить здесь, а не дублироваться в доменных модулях.

## Ориентир

Смотри существующие модули в `src/entrypoints/http/common/`.
