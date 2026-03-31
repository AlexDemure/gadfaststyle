---
description: Run the project delivery pipeline for a code generation task
agent: delivery-manager
subtask: true
---
Запусти полный агентный пайплайн кодогенерации для этой задачи.

Задача: $ARGUMENTS

Требования к выполнению:

- Используй проектные агенты и знания из `.ai/agents` и `.ai/knowledge`.
- Создай runtime-артефакты в `.ai/runtime/tasks/<YYYY-MM-DD>_<slug>/`.
- Выполни этапы intake -> architecture -> planning -> implementation -> tests -> review -> report.
- Если ревью возвращает обязательные замечания, запусти следующий цикл доработки.
- По умолчанию не делай больше 3 циклов implement/review.
- В конце дай краткий итог по результату пайплайна и пути к созданной runtime-папке.
