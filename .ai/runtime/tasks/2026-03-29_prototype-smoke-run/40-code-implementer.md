## Agent

code-implementer

## Task Request

Задача: prototype smoke run

## Instruction

## Назначение

`code-implementer` вносит production-изменения по техническому плану.

## Файлы пакета

- [rules.md](./rules.md) - правила для `code-implementer`.

## Rules

## Правила

- Агент опирается на технический план и релевантный production-код.
- Агент вносит минимальные правки в нужные слои без лишних абстракций.
- В артефакт этапа попадают текстовый лог изменений и fenced-блоки production-кода с путями.
- После изменений агент запускает `python .scripts/lints/run.py` и фиксирует результат.
- Агент не пишет тесты, кроме минимальной техподготовки для тестируемости.

## Inputs

### 30-task-orchestrator.md

## Agent

task-orchestrator

## Task Request

Задача: prototype smoke run

## Instruction

## Назначение

`task-orchestrator` преобразует задачу в технический план по слоям и шагам.

## Файлы пакета

- [rules.md](./rules.md) - правила для `task-orchestrator`.

## Rules

## Правила

- Агент опирается на артефакт архитектурного анализа, если он уже создан.
- Каждая подзадача должна содержать целевой путь, ожидаемое изменение, зависимости и критерий готовности.
- Обязательные изменения отделяются от optional.
- Технический план не смешивается с итоговым отчетом.

## Inputs

### 20-project-architect.md

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

## Result

task-orchestrator produced `30-task-orchestrator.md`.

## Result

code-implementer produced `40-code-implementer.md`.
