## Описание

`test_units` описывает unit-тесты.

## Правила

- Unit-тест покрывает локальное поведение модуля без полноценного интеграционного окружения.
- Размещай unit-тесты в зеркальной структуре относительно тестируемого пакета.
- Если сценарий уже закрывается интеграционным HTTP-тестом, не дублируй его unit-тестом без причины.
- Тест оформляй в стиле `given / when / then`, если это не ухудшает читаемость.

## Примеры

```python
class TestLocalizationDictionary:
    def given(self) -> None: ...

    def when(self, locale: Locale) -> Localization:
        return localization(locale)

    def then(self) -> None: ...
```
