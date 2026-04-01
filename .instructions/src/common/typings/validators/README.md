## Описание

`typings/validators` описывает общие валидаторы типов и значений.

## Правила

- Каждый валидатор проверяет один тип данных или один инвариант.
- Валидатор не должен зависеть от бизнесовых сущностей.
- Ошибки валидации держи согласованными по стилю и сигнатурам.

## Примеры

```python
from src.common.typings.validators import date
from src.common.typings.validators import urls
```
