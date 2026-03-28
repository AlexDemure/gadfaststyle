# Infrastructure: Monitoring

## Что входит в раздел

- `src/infrastructure/monitoring/asyncio/`
- `src/infrastructure/monitoring/health/`
- `src/infrastructure/monitoring/logging/`

## Назначение

`monitoring` содержит технические клиенты и утилиты для healthcheck, logging и runtime-monitoring.

## Базовые правила

- Новые monitoring-компоненты должны повторять структуру ближайшего раздела: `client.py`, `setup.py` и связанные подпапки, если они уже используются.
- Не смешивай прикладную бизнес-логику с monitoring-кодом.
- Если компонент подключается в lifecycle приложения, это должно быть видно в `bootstrap/server.py`.

## Ориентир

Смотри ближайший раздел в `src/infrastructure/monitoring/`.
