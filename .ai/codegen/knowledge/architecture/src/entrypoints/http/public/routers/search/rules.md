## Правила

- Используй `search.py` для ручек выборки коллекции данных в `public`.
- Handler называется `query`.
- В request-схеме используй `filters`, `sorting`, `pagination`.
- Если пагинация не нужна, поле `pagination` не добавляй.
- Endpoint только вызывает `usecase(**body.deserialize())`.
