## Описание

`schemas` описывает system HTTP-схемы.

## Правила

- Схемы одного домена группируй в одном модуле, если пакет уже следует этой форме.
- Для request используй базовые классы из `http/common`.
- Для response используй `Response`.
- Имена схем строй как `<Operation><Entity>`.
- Не копируй `public`-схемы механически: учитывай отличия `system`-контура.
- Публичные схемы экспортируй через `schemas/__init__.py`.

## Примеры

```python
class SearchAccount(System, Request, Query):
    filters: SearchAccountFilters
    sorting: SearchAccountSorting
    pagination: SearchAccountPagination


class Accounts(System, Paginated, Response):
    items: list[Account]
```
