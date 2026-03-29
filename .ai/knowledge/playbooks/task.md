## Типовой поток задачи

| Шаг | Действие | Инструкции | Результат |
| --- | --- | --- | --- |
| 1 | Зафиксируй постановку задачи. | [../instruction.md](../instruction.md), [../rules.md](../rules.md) | Понятна цель и область изменений. |
| 2 | Собери входной контекст через `delivery-manager`. | [../agents/10-delivery-manager/instruction.md](../agents/10-delivery-manager/instruction.md) | Определены затронутые слои и стартовый контекст. |
| 3 | Собери архитектурный контекст. | [../agents/20-project-architect/instruction.md](../agents/20-project-architect/instruction.md), [../architecture/instruction.md](../architecture/instruction.md) | Готов архитектурный контекст и `Todo List`. |
| 4 | Сформируй технический план. | [../agents/30-task-orchestrator/instruction.md](../agents/30-task-orchestrator/instruction.md) | Готов технический план по слоям и шагам. |
| 5 | Реализуй код. | [../agents/40-code-implementer/instruction.md](../agents/40-code-implementer/instruction.md) | Внесены production-изменения. |
| 6 | Покрой сценарий тестами. | [../agents/50-test-writer/instruction.md](../agents/50-test-writer/instruction.md) | Добавлены или обновлены тесты. |
| 7 | Проведи ревью. | [../agents/60-code-reviewer/instruction.md](../agents/60-code-reviewer/instruction.md) | Собраны замечания и остаточные риски. |
| 8 | При необходимости повтори реализацию, тесты и ревью. | [../agents/rules.md](../agents/rules.md), [../reports/rules.md](../reports/rules.md) | Замечания закрыты или явно зафиксированы. |
| 9 | Собери итоговый отчет. | [../agents/70-report-compiler/instruction.md](../agents/70-report-compiler/instruction.md), [../reports/instruction.md](../reports/instruction.md) | Сформирован итоговый артефакт задачи. |
