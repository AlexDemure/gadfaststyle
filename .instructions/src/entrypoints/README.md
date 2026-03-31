## Описание

`entrypoints` описывает точки входа в приложение.

## Правила

- Каждый entrypoint изолирует транспорт или механизм запуска от `application`.
- HTTP-код держи в `http/`.
- Новый transport добавляй отдельным пакетом, а не смешивай с существующим.
- В `entrypoints` не размещай бизнесовую логику usecase.

## Примеры

```python
from src.entrypoints.http.public.registry import registry
```
