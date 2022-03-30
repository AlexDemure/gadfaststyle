
## Мой стиль написания кода в FastAPI
### **Правила написания когда в Python**
## IDE ```PyCharm```

## PEP8

```Длина строки 120 символов```
```Отсуп 1 таб```
```Mypy```
```Flake8```


## Импорты

```Isort```
```Оптимизация импортом от PyCharm```

## Комментарии

### Однострочные докстринги
```
"""Получение списка пользователей."""
```

### Многострочные докстринги (как правило использую только в описании ручек API).
```
"""
Получение списка пользователей.

*Бизнес-логика*:
    - Взависимости от роли отдаются разные сеты данных.
*Валидация*:
    - Пользователь должен иметь роль Администратора или Менеджера.
"""
```

### Инлайновые комментарии
**Стараюсь их не писать**

## Строковые литералы и форматирование
```
f'Users count: {users_count}'
```

## Код в ```__init__.py```
**Как правило ничего в нем не пишу**

## Вызов функций и аргументы
Если функция принимает не большое количество аргументов игнорирую явную передачу аргументов
```
service_accounts.get_account_by_id(id)
```
Если функция принимает большое количество аргументов делаю явную передачу аргументов
```
service_accounts.create_account_by_manager(
    manager=manager,
    account_data=account_data,
    db=db,
    ....
)
```

## REST API
При реализации ручек для потребителей API описываю в ручке следущее:
- ```summary``` - краткое описание ручки
- ```status_code``` - успешый конечный код  
- ```response_model``` - Возвращаемая схема данных Pydantic
- ```responses``` - Все возможные варианты ответы ручки кроме серверных (500-х)
- ```Многострочные докстринги``` - Описываю полное описание ручки вместе с бизнес-логикой которая должна быть выполнена и валидация данных.

```
@router.get(
    "/{account_id}",
    summary='Get account by id',
    status_code=status.HTTP_200_OK,
    response_model=AccountData,
    responses={
        **USER_BASE_RESPONSES,
        status.HTTP_200_OK: {"description": BaseMessage.obj_data.value},
        status.HTTP_404_NOT_FOUND: {
            "model": MessageErrorSchema,
            "description": AccountErrors.account_not_found.docs_response
        },
    },
)
async def get_account_by_id_request(account_id: int) -> AccountData:
    """
    Get account by id.

    *Business-logic*:
        -  Account must be in database
    """

    return await service_accounts.get_account_by_id(account_id)

```
Префикс _request делается чтобы не получить проблему с неймингом при вызове из слоя Logic если импортируется только одна функция из слоя.

## Как ходят данные в проекте
![](https://habrastorage.org/webt/lo/2p/sa/lo2psa2bbtir0p1caxdfcgmymkw.png)

## Композиция файлов в проекте
### **API | Routes**
- Прием данных
- Отдача данных

### **Logic | Servives**
- Принимают данные из слоя Routes
- Делают бизнес-проверки (например наличие пользователя по ID)
- Поднимают HTTP исключения
- Общаются со слоями Crud, Clients, Modules
- Возвращают Pydantic объект в слой Routes

### **Core**
Ядро приложение с настройками.
```
    - config.py  # Все настройки и параметры приложения
    - main.py  # Главный модуль приложения FastApi object
    - middleware.py
    - scheduler.py  # CRON задачи приложения
    - urls.py # Подключение роутов приложения
```
### **DB**
Находятся конфигурационные параметры и настройки БД
### **Enums** и **Schemas**
Выделены отдельной папкой на практике показало более удобное использование и переиспользование их в других модулях.
### **Modules**
Папка предназначена для хранения отдельных модулей системы которыми могут выступать интеграции с другими системами как Zoom, Stripe и т.д.
Процесс интеграции с другими системами не всегда позволяет написать код в общем стиле из-за этого проще вынести в отдельную папку.
### **Clients**
Если у вас есть собственные сервисы с которыми происходит общение например по HTTP тогда в этой папке будет какой-нибудь базовый HTTP-класс от которого будут наследоваться другие клиенты и общаться с сервисами.
###  **Serializer**
Подгонка данных из табличных объектов в Pydantic объекты.
