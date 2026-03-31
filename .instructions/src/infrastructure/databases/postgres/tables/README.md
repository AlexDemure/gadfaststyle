## Описание

`tables` описывает SQLAlchemy tables для Postgres.

## Правила

- Файл таблиц определяется доменом, а не количеством таблиц внутри него.
- Таблицы одного домена храни в одном файле домена.
- Таблица описывает только persistence-форму данных.
- Имена колонок и constraints держи согласованными с доменной сущностью и миграциями.
- Публичные таблицы экспортируй через `tables/__init__.py`.

## Примеры

```python
class Account(Base):
    __tablename__ = "account"

    id = Column(BigInteger, primary_key=True)
    external_id = Column(String(length=LENGTH_SMALL_STR), nullable=False, unique=True)
    created = Column(DateTime(timezone=True), nullable=False)
```
