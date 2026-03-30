## Назначение

`agents` описывает роли агентного конвейера.

## Файлы пакета

- [RULES.MD](./RULES.MD) - общие правила для агентных ролей.
- [10-delivery-manager/INSTRUCTION.MD](./10-delivery-manager/INSTRUCTION.MD) - входной агент.
- [20-project-architect/INSTRUCTION.MD](./20-project-architect/INSTRUCTION.MD) - архитектурный анализ.
- [30-task-orchestrator/INSTRUCTION.MD](./30-task-orchestrator/INSTRUCTION.MD) - технический план.
- [40-code-implementer/INSTRUCTION.MD](./40-code-implementer/INSTRUCTION.MD) - production-реализация.
- [50-test-writer/INSTRUCTION.MD](./50-test-writer/INSTRUCTION.MD) - тестовое покрытие.
- [60-code-reviewer/INSTRUCTION.MD](./60-code-reviewer/INSTRUCTION.MD) - код-ревью.
- [70-report-compiler/INSTRUCTION.MD](./70-report-compiler/INSTRUCTION.MD) - финальный отчет.

## Контракт роли

- Каждый agent package обязан содержать `INSTRUCTION.MD`, `RULES.MD`, `INPUT.MD`, `OUTPUT.MD`, `SKILL.MD`.
- `INPUT.MD` задает, какой контекст роль должна получить до начала работы.
- `OUTPUT.MD` задает, какой артефакт и в каком содержательном виде роль обязана вернуть.
- `SKILL.MD` задает operational workflow роли и ссылки на обязательные knowledge-документы.
