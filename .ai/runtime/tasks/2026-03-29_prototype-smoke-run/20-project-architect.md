## Agent

project-architect

## Task Request

Задача: prototype smoke run

## Instruction

## Назначение

`project-architect` собирает архитектурный контекст задачи и формирует todo-list.

## Файлы пакета

- [rules.md](./rules.md) - правила для `project-architect`.

## Rules

## Правила

- Агент читает релевантные инструкции из `.ai/knowledge/architecture/src/` и `.ai/knowledge/architecture/tests/`.
- Агент анализирует существующий код и не проектирует новую архитектуру поверх текущей.
- Агент фиксирует путь данных и точки размещения новых файлов.
- Результат должен содержать архитектурный контекст и `Todo List`.
- `Todo List` оформляется таблицей `Status | Executor | Description`.
- Каждый пункт создается со статусом `todo`.

## Inputs

### 10-delivery-manager.md

## Agent

delivery-manager

## Task Request

Задача: prototype smoke run

## Instruction

## Назначение

`delivery-manager` принимает бизнесовую задачу и запускает полный агентный конвейер.

## Файлы пакета

- [rules.md](./rules.md) - правила для `delivery-manager`.

## Rules

## Правила

- Агент сам определяет затронутые слои и релевантные инструкции.
- Агент фиксирует исходную постановку и стартовый контекст задачи.
- Агент инициирует архитектурный анализ, планирование, реализацию, тесты, ревью и сборку отчета, если сценарий требует полный процесс.
- Агент не перекладывает на пользователя разбор слоев, файлов и `.ai`-инструкций.
- Для HTTP-задач по умолчанию требуется integration coverage.

## Inputs

_none_

## Result

delivery-manager produced `10-delivery-manager.md`.

## Result

project-architect produced `20-project-architect.md`.
