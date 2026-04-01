# src/bootstrap/server.py

## Статус

- created_at: 2026-04-01 12:05:35
- system_analyst_updated_at: null
- team_lead_synced_at: null
- backend_synced_at: null
- tester_synced_at: null
- spec_sync_synced_at: 2026-04-01 12:05:35

## Назначение

Поднять сервер приложения и собрать рантайм HTTP-сервиса.

## Поведение

Модуль собирает приложение FastAPI, подключает маршруты, middleware и жизненный цикл сервиса.

## Входы

- `_app`
- `_`
- `error`

## Выходы

- `typing.Any`
- `HTMLResponse`
- `dict[typing.Any, typing.Any]`
- `JSONResponse`
- `None`

## Зависимости

- `asyncio`
- `contextlib`
- `typing`
- `uvicorn`
- `fastapi: Depends`
- `fastapi: FastAPI`
- `fastapi: Request`
- `fastapi.middleware.cors: CORSMiddleware`
- `fastapi.openapi.docs: get_redoc_html`
- `fastapi.openapi.docs: get_swagger_ui_html`
- `fastapi.responses: HTMLResponse`
- `fastapi.responses: JSONResponse`
- `fastapi.staticfiles: StaticFiles`
- `src.common.http.collections: HTTPError`
- `src.entrypoints.http: router`
- `src.entrypoints.http.common.deps: basic`
- `src.framework.background: background`
- `src.framework.openapi: OpenAPI`
- `src.infrastructure.databases.postgres: postgres`
- `src.infrastructure.monitoring.asyncio.detector: detector`
- `src.infrastructure.monitoring.health: health`
- `src.infrastructure.monitoring.logging: logger`
- `src.infrastructure.storages.redis: redis`

## Ограничения

- Модуль должен оставаться в границах своего слоя и каталога.
- Модуль не должен нарушать правила импортов и зависимостей из `.instructions/src/`.
