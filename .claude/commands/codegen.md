Ты — оркестратор pipeline кодогенерации. Запусти полный цикл разработки для задачи: $ARGUMENTS

## Подготовка

1. Определи slug задачи: короткий kebab-case из 2-4 слов на основе задачи (например `update-accounts-endpoint`).
2. Создай папку задачи: `.ai/runtime/tasks/<YYYY-MM-DD>_<slug>/` где дата — сегодняшняя.
3. Сохрани путь к папке — он передаётся каждому агенту.

## Pipeline

Запускай агентов последовательно через Agent tool. Каждому передавай:
- Исходную задачу
- Путь к папке задачи
- Артефакты предыдущих этапов (содержимое файлов или ссылку на них)

### Этап 1 — delivery-manager
Запусти subagent_type: `delivery-manager`.
Результат: файл `10-delivery-manager.md` в папке задачи.

### Этап 2 — project-architect
Запусти subagent_type: `project-architect`.
Передай: задачу + содержимое `10-delivery-manager.md`.
Результат: файл `20-project-architect.md`.

### Этап 3 — task-orchestrator
Запусти subagent_type: `task-orchestrator`.
Передай: задачу + `10-delivery-manager.md` + `20-project-architect.md`.
Результат: файл `30-task-orchestrator.md`.

### Цикл реализации (максимум 5 итераций суммарно)

Веди счётчик `iteration = 0`. Имена файлов для повторных итераций:
- iteration=0: `40`, `50`, `60`
- iteration=1: `41`, `51`, `61`
- iteration=2: `42`, `52`, `62`
- и т.д.

#### Шаг A — code-implementer
Запусти subagent_type: `code-implementer`.
Передай: технический план + архитектурный контекст + замечания reviewer (если iteration > 0).
Укажи агенту имя файла для записи: `4{iteration}-code-implementer.md`.
Результат: файл `4{iteration}-code-implementer.md`.

#### Шаг B — test-writer
Запусти subagent_type: `test-writer`.
Передай: технический план + артефакт implementer текущей итерации.
Укажи агенту имя файла для записи: `5{iteration}-test-writer.md`.
Результат: файл `5{iteration}-test-writer.md`.

#### Шаг C — code-reviewer
Запусти subagent_type: `code-reviewer`.
Передай: технический план + артефакт implementer + артефакт test-writer текущей итерации.
Укажи агенту имя файла для записи: `6{iteration}-code-reviewer.md`.
Результат: файл `6{iteration}-code-reviewer.md`.

#### Решение по циклу
- Прочитай `Review Status` из файла ревью.
- Если `approved` → выход из цикла.
- Если `changes_required` И `iteration < 4` → `iteration += 1`, повтори цикл.
- Если `changes_required` И `iteration >= 4` → выход из цикла с пометкой что лимит итераций исчерпан.

### Этап 4 — report-compiler
Запусти subagent_type: `report-compiler`.
Передай: путь к папке задачи и список всех созданных файлов.
Результат: файл `70-report-compiler.md`.

## Завершение

После того как `report-compiler` завершит работу, сообщи пользователю:
- Путь к папке задачи
- Итоговый статус (approved / лимит итераций)
- Количество итераций цикла
- Список созданных файлов
