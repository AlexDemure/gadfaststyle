# 20 Project Architect

## Architecture Context

- Legacy `list` для `account` проходит через system HTTP-контур.
- Цепочка, которую нужно удалить:
  - `src/application/usecases/accounts/list.py`
  - `src/entrypoints/http/system/deps/accounts/list.py`
  - `src/entrypoints/http/system/routers/accounts/list.py`
  - подключения домена `accounts` в `system/routers/accounts/registry.py` и `system/routers/registry.py`
  - schema export `src/entrypoints/http/system/schemas/__init__.py`
- После удаления ручки нельзя оставлять пустой домен `accounts` в `system/deps/` и `system/routers/`.
- Верхний `system`-контур должен остаться корректным после удаления включения `accounts`.

## Todo List

| Status | Executor | Description |
|---|---|---|
| `todo` | `40-code-implementer` | Удалить usecase `src/application/usecases/accounts/list.py`. |
| `todo` | `40-code-implementer` | Удалить system dependency и router для `account list`. |
| `todo` | `40-code-implementer` | Удалить подключения домена `accounts` из system registry и убрать мертвые импорты. |
| `todo` | `40-code-implementer` | Если после удаления ручки папки `src/entrypoints/http/system/deps/accounts/` и `src/entrypoints/http/system/routers/accounts/` становятся пустыми, удалить их. |
| `todo` | `50-test-writer` | Проверить, есть ли зеркальные system-тесты для этой ручки, и удалить их; если тестового домена после этого не остается, удалить и пустую тестовую папку. |
| `todo` | `40-code-implementer`, `50-test-writer` | Выполнить доступные локальные проверки и зафиксировать ограничения окружения. |
| `todo` | `60-code-reviewer` | Провести ревью итогового удаления и подтвердить, что мусорных артефактов не осталось. |
