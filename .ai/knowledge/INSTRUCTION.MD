## Назначение

`knowledge` описывает human-readable и LLM-readable знания агентной системы.

## Файлы пакета

- [RULES.MD](./RULES.MD) - общие правила knowledge-слоя.
- [rules/CORE.MDC](./rules/CORE.MDC) - базовые правила для всех задач.
- [rules/PYTHON.MDC](./rules/PYTHON.MDC) - Python-правила.
- [architecture/INSTRUCTION.MD](./architecture/INSTRUCTION.MD) - архитектурные инструкции проекта.
- [reports/INSTRUCTION.MD](./reports/INSTRUCTION.MD) - формат отчетных артефактов.

## Контракт пакетов

- Для knowledge-пакетов фиксируй назначение пакета в `INSTRUCTION.MD`.
- Правила и ограничения храни в `RULES.MD`.
- Зависимости knowledge-пакета, если они есть, храни в `DEPENDENCIES.MD`.
- Примеры и эталоны формы, если они нужны, храни в `EXAMPLES.MD`.
