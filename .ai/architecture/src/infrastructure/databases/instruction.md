# Infrastructure: Databases

## Что входит в раздел

- `src/infrastructure/databases/orm/`
- `src/infrastructure/databases/postgres/`

## Навигация

- Для ORM-общих частей смотри `src/infrastructure/databases/orm/`.
- Для прикладной работы с Postgres и сущностями смотри:
  - `.ai/architecture/src/infrastructure/databases/postgres/instruction.md`
  - и затем вложенные инструкции `tables / crud / adapters`

## Базовые правила

- Usecase работает с adapter/repository, не с CRUD напрямую, если домен уже следует этой форме.
- Если появляется новая сущность, создавай все обязательные уровни инфраструктуры БД, а не только один файл.
- Если нужна миграция, она идет отдельно в `src/infrastructure/databases/postgres/migrations/versions/`.
