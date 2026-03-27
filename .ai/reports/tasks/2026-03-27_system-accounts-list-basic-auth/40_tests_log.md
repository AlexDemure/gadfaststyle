# Tests Log

## Добавленные или обновленные тесты

- `tests/test_integrations/test_entrypoints/test_http/test_system/test_accounts/test_list.py` - happy path списка аккаунтов и unauthorized сценарий

## Покрытые сценарии

- Корректный `http-basic` возвращает список аккаунтов
- Некорректный `http-basic` возвращает `401`
- `external_id` возвращается в расшифрованном виде

## Непокрытые риски

- Не добавлен отдельный тест на пагинацию по нескольким страницам
