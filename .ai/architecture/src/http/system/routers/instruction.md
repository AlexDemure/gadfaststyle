# HTTP System: Routers

## Что входит в раздел

- `src/entrypoints/http/system/routers/`
- `src/entrypoints/http/system/routers/registry.py`

## Базовые правила

- В каждом файле операции создается `router = APIRouter()`.
- Не объединяй несколько операций в один router-файл.
- Обработчик обычно называется `command` для mutation и `query` для search-ручек, если рядом не принят другой явный паттерн.
- Endpoint ничего не знает о БД и инфраструктуре напрямую, он только принимает схему и вызывает usecase.
- Формат URL и регистрация домена должны повторять существующий паттерн `system`.
- Если добавляется новый домен, подключи его через `registry.py`.

## Навигация по операциям

- `.ai/architecture/src/http/system/routers/operations/create.md`
- `.ai/architecture/src/http/system/routers/operations/delete.md`
- `.ai/architecture/src/http/system/routers/operations/update.md`
- `.ai/architecture/src/http/system/routers/operations/search.md`
- `.ai/architecture/src/http/system/routers/operations/get.md`

## Ориентир

Сохраняй ту же форму, что и в `public`, но проверяй ближайшую реализацию внутри `src/entrypoints/http/system/routers/`.
