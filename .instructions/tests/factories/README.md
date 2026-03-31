## Описание

`factories` описывает тестовые фабрики.

## Правила

- `factories` зеркалит структуру `src` по слоям и пакетам.
- Фабрики размещай в зеркальной структуре относительно слоя, для которого они создают данные.
- Используй фабрики для подготовки тестовых данных и связанного состояния.
- Если подходящая фабрика уже существует, расширяй ее вместо ручной подготовки данных.
- Публичные фабрики собирай через `__init__.py`.

## Примеры

```python
class Account(Factory[_Account]):
    class Meta:
        model = _Account

    external_id = LazyFunction(fake.uuid4)

    @classmethod
    def init(cls, external_id: str) -> typing.Self:
        return cls(external_id=external_id)
```
