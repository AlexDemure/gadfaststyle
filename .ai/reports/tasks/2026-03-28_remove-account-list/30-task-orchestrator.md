# 30 Task Orchestrator

## Technical Plan

1. Прочитать текущую реализацию `account list` по слоям `usecase -> deps -> router -> registry`.
2. Удалить код ручки и связанные импорты.
3. Удалить пустые доменные папки `accounts` в system HTTP-слое, если после удаления они не содержат рабочих файлов.
4. Проверить тестовый контур `test_system` и удалить зеркальные артефакты, если они относятся только к `list`.
5. Выполнить локальную compile-проверку измененных модулей.
6. Запустить `python .scripts/lints/run.py` и зафиксировать результат; если запуск невозможен из-за окружения, явно отметить это.
7. Провести ревью финального состояния.

## Completion Criteria

- В `src` нет `src.application.usecases.accounts.list`.
- В `src/entrypoints/http/system/` нет `account list` router/deps-цепочки.
- Пустые папки домена `accounts` в `system` не остаются.
- Локальные проверки зафиксированы в артефактах задачи.
