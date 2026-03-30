## Правила

- Разделяй domain collections по подпапкам.
- Domain exceptions описывай в `exceptions/`.
- Domain enum и другие наборы значений описывай в `enums/`.
- Публичные элементы collections экспортируй через `collections/__init__.py` с явными импортами и `__all__`.

## Запрещено

- Не складывай в `collections` прикладные утилиты.
- Не складывай в `collections` инфраструктурный код.
