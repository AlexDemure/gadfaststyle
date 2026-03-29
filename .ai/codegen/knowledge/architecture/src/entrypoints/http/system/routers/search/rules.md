## Правила

- Используй `search.py` для ручек выборки коллекции данных в `system`.
- Handler обычно называется `query`.
- В request-схеме используй `filters`, `sorting`, `pagination`.
- Если пагинация не нужна, не добавляй ее.
- Endpoint только вызывает `usecase(**body.deserialize())`.
