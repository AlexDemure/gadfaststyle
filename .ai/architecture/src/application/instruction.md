# Architecture: Application Layer

## Назначение

Эта папка зеркалит `src/application/` и служит входной точкой для инструкций application-слоя.

Сейчас основной фокус application-слоя в проекте:

- `src/application/usecases/`
- `src/application/utils/`

## Порядок чтения

1. Прочитай этот файл.
2. Если задача меняет бизнес-сценарий, открой `.ai/architecture/src/application/usecases/instruction.md`.
3. Если задача добавляет или меняет переиспользуемую прикладную утилиту, открой `.ai/architecture/src/application/utils/instruction.md`.
4. После базовой инструкции по usecase открой инструкцию конкретной операции:
   - `.ai/architecture/src/application/usecases/create/instruction.md`
   - `.ai/architecture/src/application/usecases/delete/instruction.md`
   - `.ai/architecture/src/application/usecases/update/instruction.md`
   - `.ai/architecture/src/application/usecases/search/instruction.md`
   - `.ai/architecture/src/application/usecases/get/instruction.md`
5. Только потом читай ближайший реальный модуль в `src/application/`.

## Что важно

- Инструкции в этой папке не заменяют чтение существующего кода, а направляют к ближайшему паттерну.
- Если операция уже реализована в соседнем домене, копируй форму оттуда, а не из абстрактного примера.
- Если в кодовой базе встречается legacy-операция `list`, не используй ее как новый стандарт. Для новых выборок ориентируйся на `search`.
- Для общего прикладного кода, который нужен нескольким usecase, используй `src/application/utils/`, а не дублируй логику по сценариям.
