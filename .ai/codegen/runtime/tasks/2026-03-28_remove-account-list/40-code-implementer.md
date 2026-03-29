# 40 Code Implementer

## Implementation Log

- Удален usecase `account list`.
- Удалены system dependency и router для `account list`.
- Удалены пустые доменные папки `src/entrypoints/http/system/deps/accounts/` и `src/entrypoints/http/system/routers/accounts/`.
- Очищен верхний system registry: убрано включение домена `accounts` и неиспользуемые импорты.
- Очищен `src/entrypoints/http/system/schemas/__init__.py` от export `Accounts`.

## Changed Files

- `src/application/usecases/accounts/list.py`
- `src/entrypoints/http/system/deps/accounts/list.py`
- `src/entrypoints/http/system/deps/accounts/__init__.py`
- `src/entrypoints/http/system/routers/accounts/list.py`
- `src/entrypoints/http/system/routers/accounts/__init__.py`
- `src/entrypoints/http/system/routers/accounts/registry.py`
- `src/entrypoints/http/system/routers/registry.py`
- `src/entrypoints/http/system/schemas/__init__.py`

## Code Artifacts

```diff
# path: src/application/usecases/accounts/list.py
-from src.application.utils import account
-from src.decorators import sessionmaker
-from src.domain.models import Account
-from src.infrastructure.databases.orm.sqlalchemy.queries import Pagination
-from src.infrastructure.databases.orm.sqlalchemy.queries import Sorting
-from src.infrastructure.databases.orm.sqlalchemy.session import Session
-from src.infrastructure.databases.postgres import adapters
-from src.infrastructure.security.encryption import encryption
-
-class Repository:
-    def __init__(self, session: Session) -> None:
-        self.account = adapters.repositories.Account(session)
-
-class Security:
-    def __init__(self) -> None:
-        self.encryption = encryption
-
-class Container:
-    def __init__(self, repository: Repository, security: Security) -> None:
-        self.repository = repository
-        self.security = security
-
-class Usecase:
-    def __init__(self) -> None:
-        self.container: Container | None = None
-
-    def build(self, session: Session) -> None:
-        self.container = Container(repository=Repository(session), security=Security())
-
-    @sessionmaker.read
-    async def __call__(self, session: Session, limit: int, offset: int) -> tuple[list[Account], int]:
-        self.build(session)
-
-        accounts, total = await self.container.repository.account.paginated(
-            filters=[],
-            sorting=[Sorting.desc("created")],
-            pagination=Pagination.page(limit=limit, offset=offset),
-        )
-
-        return [
-            account.decrypt(
-                decrypter=self.container.security.encryption.decrypt,
-                account=_account,
-            )
-            for _account in accounts
-        ], total
```

```diff
# path: src/entrypoints/http/system/routers/registry.py
-from fastapi import Depends
-
-from src.entrypoints.http.common.deps import basic
 from src.framework.routing import APIRouter
-
-from . import accounts
-
 
 router = APIRouter(prefix="/api/-")
-
-router.include_router(accounts.router, tags=["Accounts"], dependencies=[Depends(basic)])
```

```diff
# path: src/entrypoints/http/system/schemas/__init__.py
-from .accounts import Accounts
-
-
-__all__ = [
-    "Accounts",
-]
```

## Checks

- `python3 -m compileall src/entrypoints/http/system src/application/usecases/accounts` -> success
- `python .scripts/lints/run.py` -> not executable in current environment

```text
Traceback (most recent call last):
  File "/home/alex/git/gadfaststyle/.scripts/lints/run.py", line 6, in <module>
    import typer
ModuleNotFoundError: No module named 'typer'
```
