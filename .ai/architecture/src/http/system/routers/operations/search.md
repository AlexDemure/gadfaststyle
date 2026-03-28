# HTTP System Router Operation: Search

Используй `search.py` для ручек выборки коллекции данных в `system`, если такой паттерн уже нужен домену.

- Handler обычно называется `query`.
- В request-схеме используй `filters`, `sorting`, `pagination`.
- Если пагинация не нужна, не добавляй ее.
- Redis-кеширование используй только если это соответствует текущему паттерну `system`.
- Endpoint только вызывает `usecase(**body.deserialize())`.
- Дальше usecase должен прокинуть словари поиска в adapter/CRUD без сборки query-builder объектов для бизнес-ручки `:search`.
