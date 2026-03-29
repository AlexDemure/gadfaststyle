## Назначение

`engine` содержит исполняемый код агентного runtime.

## Состав

- `pyproject.toml` - зависимости и package metadata.
- `main.py` - локальная точка входа для запуска `python main.py "{описание задачи}"`.
- `src/` - код orchestration runtime на LangGraph.

## Команды

```bash
cd .ai/engine && python3 main.py validate
cd .ai/engine && python3 main.py "починить авторизацию с учетом кириллицы"
```

## Текущее состояние

- `spec` валидируется и компилируется в runtime pipeline.
- `knowledge` используется как единый источник инструкций, а его bundle задается декларативно через `spec/knowledge.yaml`.
- Engine запускает multi-agent pipeline через `langgraph`.
- LLM-вызовы идут через OpenAI-adapter со structured output.
- Trace-наблюдаемость ожидает стандартную конфигурацию LangSmith через env.
