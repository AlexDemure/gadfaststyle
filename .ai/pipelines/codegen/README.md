## Назначение

`pipeline` содержит опциональный исполняемый код агентного runtime на Python и LangGraph.

## Состав

- `pyproject.toml` - зависимости и package metadata.
- `main.py` - локальная точка входа для запуска `python main.py "{описание задачи}"`.
- `main.py` содержит весь orchestration runtime и hardcoded pipeline wiring.
- `spec/` пока остается как задел под постепенный вынос конфигурации из кода.

## Команды

```bash
cd .ai/pipelines/codegen && python3 main.py validate
cd .ai/pipelines/codegen && python3 main.py "починить авторизацию с учетом кириллицы"
```

## Текущее состояние

- Текущий pipeline описан явно в `main.py`, без обязательной загрузки из `spec`.
- `knowledge` используется как единый источник инструкций, но остается самостоятельным слоем без зависимости от `pipeline`.
- Pipeline запускает multi-agent workflow через `langgraph`.
- LLM-вызовы идут через OpenAI-adapter со structured output.
- Trace-наблюдаемость ожидает стандартную конфигурацию LangSmith через env.
