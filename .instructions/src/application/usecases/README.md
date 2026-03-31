## Описание

`usecases` описывает application-сценарии.

## Правила

- Usecase оформляй отдельным файлом операции внутри доменной папки.
- Основной класс называй `Usecase`.
- Зависимости собирай через `build(session)` и `self.container`, если этот каркас уже принят в пакете.
- Вызов сценария реализуй через `__call__(...)`.
- Не тащи в usecase HTTP-детали, SQL и прямую работу с table или CRUD, если домен уже работает через adapter.

## Примеры

```python
class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session))
```
