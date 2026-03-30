## Правила

- `knowledge` хранит только инструкции, правила, примеры и playbook-ы.
- `knowledge` не хранит исполняемый код orchestration runtime.
- `knowledge` не хранит machine-readable pipeline config.
- Package format внутри `knowledge` остается единым: `INSTRUCTION.MD`, `RULES.MD`, `DEPENDENCIES.MD`, `EXAMPLES.MD`, если они нужны пакету.
- Агентные роли хранятся отдельно в `.ai/agents/` и не смешиваются с `knowledge`.
- `knowledge` задает общий контекст для ролей и pipeline, но не описывает жизненный цикл конкретного агента.
