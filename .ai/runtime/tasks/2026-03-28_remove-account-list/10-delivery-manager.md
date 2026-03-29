# 10 Delivery Manager

## Business Request

`Задача: Удали ручку list для сущности account.`

## Pipeline Start

- Запущен полный конвейер для удаления legacy `list`-ручки `account`.
- Затронутые зоны определены предварительно:
  - `src/application/usecases/accounts/`
  - `src/entrypoints/http/system/`
  - `tests/test_integrations/test_entrypoints/test_http/test_system/`
- Ожидаемые этапы: `20-project-architect`, `30-task-orchestrator`, `40-code-implementer`, `50-test-writer`, `60-code-reviewer`, `70-report-compiler`.
