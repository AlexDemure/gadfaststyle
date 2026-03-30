## Правила

- `search` возвращает коллекцию данных.
- Не дублируй в usecase разбор `filters`, `sorting`, `pagination`, если они уже подготовлены схемой.
- Не собирай в usecase builder-объекты `Filter`, `Sorting`, `Pagination` для бизнес-ручек `:search`.
- Основная логика поиска должна собираться в repository adapter и entity-specific CRUD `search(...)`.
- Для новых сценариев не используй `list` как паттерн выборки.

## Допустимо

- Прокидывание `filters`, `sorting`, `pagination` как словарей в repository adapter.
- Пост-обработка результата перед `return`.
- Возврат `tuple[list[Model], int]`, если сценарий поддерживает пагинацию.

