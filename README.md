<p align="center">
  <a href="https://github.com/AlexDemure/gadfaststyle">
    <a href="https://ibb.co/TqkGRPCN"><img src="https://i.ibb.co/sJ24QsBX/logo.png" alt="logo" border="0"></a>
  </a>
</p>

<p align="center">
  FastAPI backend with spec-driven development workflow
</p>

---

# gadfaststyle

`gadfaststyle` — backend-проект на `FastAPI`, в котором разработка ведется через `spec.md`.

## Структура

- `src/` — production-код сервиса.
- `tests/` — тесты проекта.
- `.instructions/` — правила проекта, архитектура, code style и ограничения по слоям.
- `.specs/` — спецификации файлов проекта.
- `.codex/` — provider-specific слой для OpenAI/Codex: агенты, команды и runtime-артефакты.
- `.templates/` — шаблон развертывания каркаса проекта.

## Как это работает

В проекте один файл кода соответствует одному `spec.md`.

- `.instructions/src/` и `.instructions/tests/` зеркалят структуру каталогов `src/` и `tests/`.
- `.specs/src/` и `.specs/tests/` зеркалят файлы `src/` и `tests/`.
- `spec.md` описывает, как должен работать конкретный файл, но без кода.

Пример:

- `src/application/usecases/accounts/current.py`
- `.specs/src/application/usecases/accounts/current.py/spec.md`

## Команды

Для Codex команды описаны в [`.codex/README.md`](/home/alex/git/gadfaststyle/.codex/README.md).

Основные команды:

- `code: <описание задачи>` — провести разработку через `spec.md`.
- `sync` — синхронизировать `.specs/` с текущим состоянием `src/` и `tests/`.

## Поток разработки

```text
Задача
  -> system-analyst
  -> .specs/**/*.md
  -> backend -> src/
  -> tester -> tests/
  -> team-lead review
  -> .codex/runtime/code/<timestamp>_<slug>.md
```

Что делает `code`:

1. Аналитик создает или обновляет затронутые `spec.md`.
2. Backend реализует код в `src/` по этим `spec.md`.
3. Tester реализует тесты в `tests/` по этим `spec.md`.
4. Team lead проводит ревью, возвращает замечания или завершает задачу.
5. Весь процесс пишется в один runtime-файл.

## Поток синхронизации

```text
src/ + tests/
  -> spec-sync
  -> .specs/**/*.md
  -> .codex/runtime/sync/<timestamp>_sync.md
```

Что делает `sync`:

1. Сканирует `src/`, `tests/` и `.specs/`.
2. Находит расхождения между кодом и спецификациями.
3. Создает, обновляет, удаляет или перемещает `spec.md`.
4. Пишет один runtime-файл синхронизации.

Исключение:

- `src/infrastructure/databases/postgres/migrations/` не документируется в `.specs/`.

## Формат spec.md

Каждый `spec.md` содержит:

- `Статус`
- `Назначение`
- `Поведение`
- `Входы`
- `Выходы`
- `Зависимости`
- `Ограничения`

В `Статус` хранятся даты и время с секундами:

- `created_at`
- `system_analyst_updated_at`
- `team_lead_synced_at`
- `backend_synced_at`
- `tester_synced_at`
- `spec_sync_synced_at`

## Runtime-артефакты

Каждый запуск команды пишет один файл:

- `.codex/runtime/code/<YYYY-MM-DD_HH-MM-SS>_<slug>.md`
- `.codex/runtime/sync/<YYYY-MM-DD_HH-MM-SS>_sync.md`

В runtime-файлах фиксируются:

- шаги агентов;
- полное содержимое затронутых `spec.md`;
- замечания ревью и итог работы.

## Зачем это нужно

Такая схема дает:

- явный слой спецификаций между задачей и кодом;
- воспроизводимую разработку через `spec.md`;
- синхронизацию ручных изменений обратно в спецификации;
- единый runtime-журнал работы агентов.
