# HTTP Public Router Operation: Create

Используй `create.py` для mutation-ручек создания в `public`.

- Handler называется `command`.
- Обычно используется `Body(...)`, `Depends(dependency)`, `status.HTTP_201_CREATED`.
- Ошибки домена подключай через `responses=errors(...)`, если это уже принято в соседних ручках.
- Endpoint только вызывает `usecase(**body.deserialize())`.
