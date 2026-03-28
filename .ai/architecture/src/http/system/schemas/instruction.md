# HTTP System: Schemas

## Что входит в раздел

- `src/entrypoints/http/system/schemas/`

## Базовые правила

- Схемы одного домена группируй в одном модуле, если это уже соответствует текущему стилю.
- Для request используй базовые классы из `src/entrypoints/http/common/schemas`.
- Для response используй `Response`.
- Наследование и базовые system-схемы повторяй по текущему паттерну `system`.
- Имена схем строятся как `<Operation><Entity>`.
- Не копируй public-схемы механически: учитывай, что у `system` может отличаться базовый класс, состав полей и сериализация.

## Ориентир

Смотри ближайшую реализацию в `src/entrypoints/http/system/schemas/`.
