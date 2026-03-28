# Architecture: Infrastructure Layer

## Назначение

Эта папка зеркалит `src/infrastructure/` и служит входной точкой для инструкций infrastructure-слоя.

Сейчас основной фокус infrastructure-слоя в проекте:

- `src/infrastructure/databases/`
- `src/infrastructure/security/`
- `src/infrastructure/storages/`
- `src/infrastructure/monitoring/`

## Порядок чтения

1. Прочитай этот файл.
2. Если задача касается БД, открой `.ai/architecture/src/infrastructure/databases/instruction.md`.
3. Если задача касается security-клиентов, открой `.ai/architecture/src/infrastructure/security/instruction.md`.
4. Если задача касается storage-клиентов, открой `.ai/architecture/src/infrastructure/storages/instruction.md`.
5. Если задача касается monitoring, открой `.ai/architecture/src/infrastructure/monitoring/instruction.md`.
6. Только потом читай ближайший реальный модуль в `src/infrastructure/`.

## Что важно

- Infrastructure изолирует внешние системы и технические реализации.
- Новый код в infrastructure должен зеркалить существующую структуру `src/infrastructure/`.
- Lifecycle, singleton setup и конфигурация должны оставаться явными и повторять текущий проектный паттерн.
