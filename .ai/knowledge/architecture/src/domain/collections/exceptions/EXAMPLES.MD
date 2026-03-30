## Эталонная форма

```python
from src.common.http.collections import HTTPError


class AccountNotFound(HTTPError): ...


class AccountBlocked(HTTPError): ...


class AccountAlreadyExists(HTTPError): ...
```

