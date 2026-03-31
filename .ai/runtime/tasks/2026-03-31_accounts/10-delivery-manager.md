# Delivery Manager Intake

- Role: `delivery-manager`
- Artifact: `10-delivery-manager.md`
- Mode: `stage-only`

## Business Requirement

Пользовательская задача: `добавить ручку обновление accounts`.

Нужно подготовить постановку для добавления HTTP-ручки обновления аккаунта в существующий модуль `accounts` без запуска полного пайплайна на этом этапе.

## Scope

Входит в задачу:
- анализ стартовой постановки для новой ручки обновления `accounts`;
- фиксация затронутых областей репозитория на верхнем уровне;
- передача контекста для следующих этапов через runtime-артефакт.

Потенциально затрагиваемые области по текущей структуре репозитория:
- `src/entrypoints/http/public/routers/accounts/` — существующие public account endpoints (`create`, `current`, `delete`);
- `src/entrypoints/http/public/deps/accounts/` — dependency wiring для usecase;
- `src/entrypoints/http/public/schemas/accounts.py` — request/response schema для public accounts;
- `src/application/usecases/accounts/` — usecase-слой account-операций;
- `src/infrastructure/databases/postgres/adapters/repositories/account.py` и связанный persistence-слой;
- `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/` — integration coverage для HTTP-сценария.

Не входит в этот этап:
- архитектурное проектирование решения;
- реализация кода;
- написание тестов;
- запуск других агентов или полного pipeline.

## Constraints

- Выполняется режим `stage-only`: нужно создать только этот intake-артефакт и остановиться.
- Нельзя вызывать другие агенты.
- Нельзя запускать полный delivery pipeline.
- Нужно опираться на реальную структуру репозитория.
- Для HTTP-задач по правилам проекта ожидается integration coverage на следующих этапах.
- Из постановки пока не следует, какая именно операция обновления требуется: обновление текущего аккаунта, обновление по `id`, состав изменяемых полей и правила авторизации не заданы явно.

## Open Questions or Assumptions

- Предположение: речь идет о новой HTTP-ручке внутри существующего `accounts`-модуля, вероятнее всего в public HTTP-слое рядом с `create/current/delete`.
- Неизвестно, какой HTTP-метод и route contract ожидаются (`PATCH`, `PUT`, `/accounts:update` или иной формат), хотя текущие public routes используют command-style path вроде `/accounts:create` и `/accounts:delete`.
- Неизвестно, какие поля аккаунта разрешено менять. По текущей доменной модели `Account` явное прикладное поле — `external_id`; остальные поля выглядят системными.
- Неизвестно, должна ли ручка требовать авторизацию текущего аккаунта либо быть системной/административной операцией.
- Предположение: следующие этапы должны уточнить контракт, слой авторизации, usecase и минимальный набор integration-тестов.

## Pipeline Decision

Полный pipeline для исходной задачи в нормальном режиме требуется, но в данном запуске **не выполняется**, потому что внешний запрос явно задан как `stage-only` и ограничивает работу созданием только `10-delivery-manager.md`.
