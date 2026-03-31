# Task Orchestrator Plan

## Task

- Original task: `добавить ручку обновление accounts`.
- Role: `task-orchestrator`.
- Artifact: `30-task-orchestrator.md`.
- This stage converts the intake and architecture context into an executable implementation and verification plan only.
- No code is implemented in this stage.

## Goal

- Add the minimal HTTP endpoint for updating `accounts` in the existing application structure.
- Reuse the current public `accounts` command-style API shape and the existing persistence update primitive.
- Keep the change as a narrow vertical slice: router, schema, dependency wiring, usecase, and integration coverage.

## Repository Facts Confirmed

- Public account routes already live in `src/entrypoints/http/public/routers/accounts/` and use command-style paths:
  - `POST /accounts:create`
  - `GET /accounts:current`
  - `DELETE /accounts:delete`
- Authenticated current-account resolution already exists through `src/entrypoints/http/common/deps/accounts/session.py` and is used by `Depends(account)`.
- Public account request/response models are centralized in `src/entrypoints/http/public/schemas/accounts.py`.
- Public usecase DI wrappers are tiny modules in `src/entrypoints/http/public/deps/accounts/`.
- The domain model in `src/domain/models/account.py` exposes `external_id`, `blocked`, and `authorization`, but only `external_id` currently looks like a user-editable business field.
- `external_id` is encrypted at rest and uniqueness is enforced in the create flow by checking the encrypted lowercase value.
- The repository base already supports `update(id=..., **kwargs)` and updates the `updated` timestamp centrally.
- Current integration coverage in `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/` only proves `create`.

## Contract Decision Gate

- The source task is underspecified. Before implementation, the executor must explicitly resolve or record these points:
1. Target surface: `public` current-account endpoint vs `system` update-by-id endpoint.
2. HTTP method: `PATCH` vs `PUT`.
3. Route path: expected command-style path, most likely `/accounts:update` if the endpoint stays in public HTTP.
4. Payload: which account fields are allowed to change.

- Default assumption if no new product input appears:
1. Public authenticated endpoint.
2. Update the current account resolved from JWT, not an arbitrary account id from the client.
3. Command-style route at `/accounts:update`.
4. Only `external_id` is mutable.
5. Use `PATCH` unless an existing project convention discovered during implementation requires `PUT`.

## Execution Constraints

- Do not introduce new storage infrastructure; build on the existing account repository and ORM update path.
- Do not widen the public contract to system-owned fields such as `blocked` or `authorization` without explicit confirmation.
- Preserve the existing public router style, dependency style, and error-contract style.
- Keep encryption and uniqueness behavior for `external_id` consistent with account creation.
- Prefer a single new usecase module over broader refactoring.

## Implementation Plan

1. Confirm the endpoint contract against the decision gate.
   - If the intended endpoint is administrative or updates arbitrary account ids, stop the public-path implementation and redirect the work to the system HTTP surface.
   - If no clarification is available, proceed with the default public current-account assumption and document it in the implementation artifact.
2. Add the public HTTP entrypoint.
   - Create a new router module in `src/entrypoints/http/public/routers/accounts/`.
   - Register it in `src/entrypoints/http/public/routers/accounts/registry.py` next to the existing `create/current/delete` routes.
   - Require authenticated account resolution with `Depends(account)`.
3. Add request and response schemas in `src/entrypoints/http/public/schemas/accounts.py`.
   - Add a request schema for the allowed mutable fields.
   - If the route returns the updated account state, reuse the current response style and keep the schema minimal.
   - If the route returns no body, use the same response-class approach as `delete`.
4. Add DI wiring in `src/entrypoints/http/public/deps/accounts/`.
   - Follow the existing one-function dependency module pattern returning the new usecase instance.
5. Add an account update usecase under `src/application/usecases/accounts/`.
   - Mirror the `create` and `delete` structure: repository container, optional security container, and `@sessionmaker.write` entrypoint.
   - Accept the current `account_id` plus validated mutable fields.
   - Normalize and encrypt `external_id` before uniqueness checks and persistence if `external_id` is in scope.
   - Skip duplicate detection when the normalized new `external_id` equals the account's current value.
   - Call repository `update(id=..., **kwargs)` so the shared base layer owns the `updated` timestamp.
6. Keep domain and persistence changes minimal.
   - Reuse the existing `Account` model and repository adapter unless implementation reveals a missing primitive.
   - Only extend lower layers if the current usecase cannot safely perform the required collision check or current-value comparison.

## Verification Plan

1. Add integration tests in `tests/test_integrations/test_entrypoints/test_http/test_public/test_accounts/` for the selected contract.
2. Minimum scenarios for the default public-path assumption:
   - successful authenticated update of the current account;
   - unauthorized request without valid auth;
   - duplicate `external_id` rejection if `external_id` is mutable;
   - no-op or same-value update behavior if contractually relevant.
3. Validate persistence effects.
   - The record is updated for the authenticated account only.
   - Stored encrypted data remains readable through the existing model flow.
   - `updated` changes through the repository base path rather than ad hoc timestamp handling in the router.
4. Run the smallest relevant test target for the new account-update scenarios.

## Deliverables For Next Stages

- New `accounts` update router registered in the public router registry if the contract remains public.
- New request schema and any minimal response schema updates in `src/entrypoints/http/public/schemas/accounts.py`.
- New dependency wrapper in `src/entrypoints/http/public/deps/accounts/`.
- New application usecase for account update.
- Integration tests for the endpoint contract and the critical failure path.

## Acceptance Criteria

- The chosen endpoint contract is explicit and matches the target HTTP surface.
- The implementation reuses existing auth, encryption, and repository update patterns instead of introducing parallel mechanisms.
- Only intended account fields are mutable.
- Duplicate `external_id` updates are rejected consistently with account creation rules.
- Integration coverage proves the happy path and the key contract failure paths.
- The change remains limited to the minimal vertical slice required for account update.

## Blockers And Escalation Rules

- Block implementation if the expected endpoint is actually update-by-id or belongs to the system API surface.
- Block widening the payload beyond `external_id` unless the field semantics and authorization model are confirmed.
- If the executor discovers an existing project convention that prefers `PUT` over `PATCH` for command-style update routes, follow the repository convention and record that decision explicitly.
