# Architecture Context

- Original task: `добавить ручку обновление accounts`.
- Intake artifact confirms this run is limited to the `project-architect` stage and does not authorize code implementation.
- The existing public HTTP `accounts` module currently exposes three routes in `src/entrypoints/http/public/routers/accounts/`: `POST /accounts:create`, `GET /accounts:current`, and `DELETE /accounts:delete`.
- Public account commands follow a command-style route naming convention with `:` in the path, so the closest existing contract shape for a new update endpoint is another command-style route alongside `create/delete`, not a REST-style `/accounts/{id}` path.
- Authentication for the current account already exists via `src/entrypoints/http/common/deps/accounts/session.py`, where `Depends(account)` resolves the current account from a JWT through `src.application.usecases.accounts.get.jwt.Usecase`.
- The domain model `src/domain/models/account.py` currently exposes `id`, `external_id`, `created`, `updated`, `blocked`, and `authorization`; only `external_id` is a clear user-editable business field in the current model, while `blocked` and `authorization` look system-owned.
- The repository stack already has generic update support in `src/infrastructure/databases/postgres/adapters/repositories/base.py` and `src/infrastructure/databases/orm/sqlalchemy/crud/base.py`, so the likely implementation path is to add an account-specific update use case on top of existing persistence primitives rather than introduce new storage infrastructure.
- Existing integration coverage for public accounts is minimal and currently only includes create flow coverage in `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_create.py`.

# Touched Layers

- Public HTTP router layer
  - `src/entrypoints/http/public/routers/accounts/create.py`
  - `src/entrypoints/http/public/routers/accounts/current.py`
  - `src/entrypoints/http/public/routers/accounts/delete.py`
  - `src/entrypoints/http/public/routers/accounts/registry.py`
  - Purpose: existing route style, auth expectations, and router registration point for the future update endpoint.
- Public HTTP schema layer
  - `src/entrypoints/http/public/schemas/accounts.py`
  - Purpose: request/response contracts for public account flows; this is the natural place for an `UpdateAccount` request schema and, if needed, a response schema.
- Public dependency wiring layer
  - `src/entrypoints/http/public/deps/accounts/create.py`
  - `src/entrypoints/http/public/deps/accounts/delete.py`
  - `src/entrypoints/http/public/deps/accounts/get.py`
  - Purpose: lightweight DI wrappers that construct account use cases for routers.
- Common auth dependency layer
  - `src/entrypoints/http/common/deps/accounts/session.py`
  - `src/entrypoints/http/common/deps/security/jwt.py`
  - `src/entrypoints/http/common/collections/errors/security.py`
  - Purpose: current-account resolution and shared authorization error contract for authenticated public endpoints.
- Application use case layer
  - `src/application/usecases/accounts/create.py`
  - `src/application/usecases/accounts/delete.py`
  - `src/application/usecases/accounts/get/jwt.py`
  - `src/application/usecases/accounts/get/external.py`
  - `src/application/usecases/accounts/search.py`
  - Purpose: reference patterns for session handling, encryption, existence checks, and account retrieval; a new update use case should match this structure.
- Domain and persistence layer
  - `src/domain/models/account.py`
  - `src/infrastructure/databases/postgres/adapters/repositories/account.py`
  - `src/infrastructure/databases/postgres/adapters/repositories/base.py`
  - `src/infrastructure/databases/postgres/tables/account.py`
  - `src/infrastructure/databases/postgres/crud/account.py`
  - Purpose: available mutable fields, encrypted attributes, and reusable update primitive.
- Verification layer
  - `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/test_create.py`
  - Purpose: existing integration-test location and style for public account HTTP scenarios.

# Proposed Architecture Direction

- Default working assumption for downstream stages: add an authenticated public command endpoint for updating the current account, most likely as `PATCH /accounts:update` or `PUT /accounts:update`, using `Depends(account)` rather than accepting an arbitrary account id from the client.
- Minimal vertical slice under that assumption:
  - add a new public router module under `src/entrypoints/http/public/routers/accounts/` and register it in `registry.py`;
  - add a request schema in `src/entrypoints/http/public/schemas/accounts.py` for allowed mutable fields;
  - add a new dependency wrapper in `src/entrypoints/http/public/deps/accounts/`;
  - add a new application use case under `src/application/usecases/accounts/` that loads update dependencies, validates business constraints, encrypts updated fields when required, and calls repository `update`;
  - reuse shared authorization error responses from the current authenticated endpoints;
  - add integration coverage in `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/` for the happy path and the key contract failures.
- If the intended operation is instead an administrative update-by-id endpoint, the architecture changes materially: the route would more likely live in the system HTTP surface, not the public one, and would need a different auth model and schema contract. That decision must be clarified before implementation.

# Todo List

| Status | Executor | Description |
| --- | --- | --- |
| todo | task-orchestrator | Convert `добавить ручку обновление accounts` into an executable plan by first fixing the missing contract details: target surface (`public` vs `system`), HTTP method, route path, and whether the endpoint updates the current account or an arbitrary account by id. |
| todo | task-orchestrator | Confirm the allowed mutable fields. Based on the current model, `external_id` is the only clear business candidate; `blocked` and `authorization` appear system-owned and should not be assumed editable from the public API without explicit product confirmation. |
| todo | code-implementer | Add the minimal router/schema/dependency/usecase slice for account update in the same style as existing `accounts` endpoints, reusing current-account auth if the contract stays public. |
| todo | code-implementer | Reuse repository `update(id=..., **kwargs)` and existing encryption flow so that encrypted fields such as `external_id` remain stored consistently and `updated` timestamp continues to be managed centrally by the repository base layer. |
| todo | code-implementer | If `external_id` is mutable, preserve uniqueness guarantees by checking for collisions against the encrypted normalized value before persisting the update. |
| todo | test-writer | Add integration tests for the chosen update endpoint in `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/`, covering at minimum a successful authenticated update, auth failure, and relevant domain validation such as duplicate `external_id` if that field is allowed. |
| todo | code-reviewer | Review for contract consistency with existing command-style routes, correct auth boundary, encrypted field handling, and regression risk around account lookup/update semantics. |

# Risks or Blockers

- The task statement is underspecified on the most important architectural axis: there is no confirmed endpoint contract yet for method, path, actor, or payload.
- The current `accounts` public API only proves one mutable business field, `external_id`; if the intended update payload includes fields not present in the current domain model, the work may require domain/schema expansion rather than only adding a new endpoint.
- There is no existing integration coverage for authenticated public `accounts` update/delete/current flows in the discovered test tree, so downstream implementation should expect to establish the testing pattern rather than copy an existing update test.
- If update should target accounts by arbitrary id, the currently suggested public-layer path becomes invalid and the implementation should be redirected to the system HTTP surface before coding starts.
- No implementation or runtime validation was performed in this stage-only run.
