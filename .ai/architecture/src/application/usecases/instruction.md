# Architecture: Application Usecases

## Что входит в раздел

- `src/application/usecases/<domain>/create.py`
- `src/application/usecases/<domain>/delete.py`
- `src/application/usecases/<domain>/update.py`
- `src/application/usecases/<domain>/search.py`
- `src/application/usecases/<domain>/get/...`

## Базовая форма usecase

- Usecase оформляется отдельным файлом операции внутри доменной папки.
- Основной класс всегда называется `Usecase`.
- Usecase хранит `self.container`.
- Зависимости собираются в `build(session)`.
- Вызов сценария реализуется через `async def __call__(...)`.
- Для чтения и записи используй текущие декораторы `@sessionmaker.read` и `@sessionmaker.write`.

Эталон общей формы:

```python
from src.decorators import sessionmaker
from src.infrastructure.databases.orm.sqlalchemy.session import Session
from src.infrastructure.databases.postgres import adapters


class Repository:
    def __init__(self, session: Session) -> None:
        self.account = adapters.repositories.Account(session)


class Container:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository


class Usecase:
    def __init__(self) -> None:
        self.container: Container | None = None

    def build(self, session: Session) -> None:
        self.container = Container(repository=Repository(session))
```

## Правила написания

- Сначала смотри соседний usecase того же домена и повторяй его форму.
- В usecase допустима orchestration-логика: проверки, вызовы репозиториев, security, сборка ответа.
- Доменные ошибки поднимай через `src.domain.collections`.
- Не переноси HTTP-детали в usecase.
- Не строй SQL и не обращайся к таблицам напрямую из usecase.
- Если в домене уже используется `Repository`, `Security`, `Container`, не вводи рядом новый стиль именования.

## Навигация по операциям

- `create` - создание новой сущности или нового состояния.
- `delete` - удаление или мягкое выключение сущности.
- `update` - изменение существующей сущности.
- `search` - выборка по `filters/sorting/pagination`, обычно с прокидыванием параметров в repository.
- `get` - точечное чтение одной сущности или варианта идентификации.

Детали по специфике каждой операции описывай только в ее собственной инструкции. Базовый файл не должен дублировать частные правила `create/delete/update/search/get`.

## Что не делать

- Не вводи новый usecase-тип `list` для новых сценариев.
- Не смешивай чтение и запись без явной причины.
- Не зашивай инфраструктурные детали выше того уровня, который уже принят в соседнем usecase.
