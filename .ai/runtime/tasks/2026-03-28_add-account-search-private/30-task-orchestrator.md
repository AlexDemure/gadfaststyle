# Task Orchestrator

## Technical Plan

1. Проверить существующий `system` HTTP-контур для `accounts` и определить, какие файлы нужно добавить или обновить для `search`.
2. Добавить usecase поиска аккаунтов с:
   - точным фильтром по `id`
   - сортировкой по `created`
   - переключением `asc` / `desc`
   - пагинацией через общий `Pagination.page(...)`
3. Добавить системные request/response схемы для `accounts:search`.
4. Подключить dependency и router в `system` registry.
5. Добавить интеграционные тесты на:
   - сортировку по `created` desc
   - сортировку по `created` asc
   - фильтр по `id`
   - пагинацию
   - unauthorized доступ
6. Выполнить доступные проверки:
   - `python3 -m compileall ...`
   - `python .scripts/lints/run.py`
   - `pytest ...`, если команда доступна в окружении
7. Сформировать review и итоговый собранный отчет.

## Notes

- Приватные ручки интерпретированы как `src/entrypoints/http/system`.
- Сигнатура и naming должны повторять уже согласованный паттерн `search`, а не `list`.
