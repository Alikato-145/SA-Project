# Tasks: A1 Authentication Foundation

**Input**: Design documents from `/specs/002-a1-auth-foundation/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

**Tests**: Required by FR-025. Write focused tests before the corresponding implementation and verify that they fail for the expected reason.

**Organization**: Tasks are grouped by user story and use the mandatory route → controller → service → repository layering.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable because it owns different files and has no dependency on an incomplete task.
- **[Story]**: User story from `spec.md`.

## Phase 1: Setup

**Purpose**: Add the minimum runtime/configuration surface without changing the frozen schema.

- [X] T001 Add the Elysia-compatible JWT dependency and update lockfile in `backend/package.json` and `backend/bun.lock`
- [X] T002 Add validated JWT secret, exact allowed origins, environment mode, eight-hour TTL, five-attempt threshold, and 15-minute lock configuration in `backend/src/core/config/env.config.ts` and `backend/src/core/config/auth.config.ts`
- [X] T003 [P] Define the database executor/transaction contract required by audited services, coordinated with Person C, in `backend/src/core/db/transaction.ts`
- [X] T004 [P] Add idempotent fixed-role bootstrap and controlled initial-Owner setup contract without schema changes in `backend/src/features/role/role.bootstrap.ts` and `backend/src/features/role/role.bootstrap.test.ts`

**Checkpoint**: Dependencies, safe environment validation, transaction executor, and canonical role setup are available.

---

## Phase 2: Foundational - Errors, request context, and audit primitives

**Purpose**: Blocking infrastructure required by every A1 use case.

- [X] T005 [P] Write failing typed-error and stable public-envelope tests in `backend/src/core/errors/error-boundary.test.ts`
- [X] T006 [P] Write failing request-ID validation/generation tests in `backend/src/core/audit/action-context.test.ts`
- [X] T007 [P] Write failing recursive secret-redaction and per-event allowlist tests covering password, temporary password, hash, token, cookie, authorization, account number/ciphertext, national ID, and passport ID in `backend/src/core/audit/audit-redaction.test.ts`
- [X] T008 Implement typed application errors, stable codes, status mapping, request IDs, and redacted error boundary in `backend/src/core/errors/application.error.ts`, `backend/src/core/errors/error-codes.ts`, `backend/src/core/errors/error-boundary.ts`, and `backend/src/shared/http/http.dto.ts`
- [X] T009 Implement action context and request-ID plugin with a maximum 100-character validated correlation value in `backend/src/core/audit/action-context.ts` and `backend/src/core/audit/request-id.plugin.ts`
- [X] T010 Implement event allowlists plus defense-in-depth recursive secret redaction in `backend/src/core/audit/audit-redaction.ts`
- [X] T011 [P] Write failing audit repository/observer tests for read success/failure, mutation receipt, one canonical row, rollback behavior, original-error preservation, and non-recursion in `backend/src/core/audit/action-observer.test.ts` and `backend/src/features/audit/audit.integration.test.ts`
- [X] T012 Implement insert-only audit repository using the shared executor and redacted DTO input in `backend/src/features/audit/audit.repository.ts`
- [X] T013 Implement action and domain observers so mutation success is atomic, failure persists after rollback, reads are audited before disclosure, and exactly one canonical row is produced in `backend/src/core/audit/action-observer.ts`, `backend/src/core/audit/domain-audit-observer.ts`, and `backend/src/features/audit/audit.service.ts`
- [X] T014 Verify Phase 2 focused tests and backend typecheck using `backend/src/core/errors/*.test.ts`, `backend/src/core/audit/*.test.ts`, and `backend/src/features/audit/*.test.ts`

**Checkpoint**: Every subsequent service can produce stable failures and mandatory redacted audit evidence.

---

## Phase 3: User Story 1 - Sign in, sign out, and current actor (Priority: P1) 🎯 MVP

**Goal**: Active users can authenticate, inspect safe current context, use an eight-hour HTTP-only cookie, and sign out.

**Independent Test**: Sign in an active account, call `/auth/me`, call one protected handler, sign out, and confirm the protected handler returns `AUTH_REQUIRED`.

### Tests for User Story 1

- [X] T015 [P] [US1] Write failing Argon2id hash/verify, dummy-hash, JWT expiry/tamper, cookie-option, and token-minimality tests in `backend/src/core/auth/password.test.ts` and `backend/src/core/auth/session-token.test.ts`
- [X] T016 [P] [US1] Write failing exact-Origin and JSON mutation content-type tests including login/logout in `backend/src/core/auth/csrf-origin.test.ts`
- [X] T017 [P] [US1] Write failing login/logout/me route contract tests for safe DTOs, cookie set/removal, stable errors, request IDs, and audit correlation in `backend/src/features/user-account/auth.routes.test.ts`

### Implementation for User Story 1

- [X] T018 [US1] Implement password hashing/dummy verification and minimal eight-hour JWT token service in `backend/src/core/auth/password.ts`, `backend/src/core/auth/session-token.ts`, and `backend/src/core/auth/auth.types.ts`
- [X] T019 [US1] Implement exact origin/content-type validation for cookie-authenticated mutations in `backend/src/core/auth/csrf-origin.ts`
- [X] T020 [US1] Implement safe account lookup, current actor projection, and fresh active-grant loading in `backend/src/features/user-account/user-account.repository.ts` and `backend/src/core/auth/authenticated-actor.ts`
- [X] T021 [US1] Implement login/logout/current-actor service commands with action observation in `backend/src/features/user-account/user-account.service.ts`
- [X] T022 [US1] Implement auth request/response contracts, pure mapper, thin controller, auth plugin, and exported routes in `backend/src/features/user-account/user-account.dto.ts`, `backend/src/features/user-account/user-account.validation.ts`, `backend/src/features/user-account/user-account.mapper.ts`, `backend/src/features/user-account/user-account.controller.ts`, `backend/src/core/auth/auth.plugin.ts`, and `backend/src/features/user-account/user-account.routes.ts`
- [X] T023 [US1] Run US1 focused tests and confirm `/auth/me` never returns password hash, attempt counters, internal lock fields, bank data, or full personal identifiers in `backend/src/features/user-account/auth.routes.test.ts`

**Checkpoint**: US1 is independently usable as the minimum authentication slice.

---

## Phase 4: User Story 2 - Atomic five-attempt lockout (Priority: P1)

**Goal**: Consecutive failures lock on attempt five for 15 minutes without lost increments under concurrency.

**Independent Test**: Exercise attempts 1, 4, 5, during lock, exactly at expiry, and after expiry with a controlled clock and concurrent requests.

### Tests for User Story 2

- [X] T024 [US2] Write failing service/integration tests for attempts 1/4/5, correct password while locked, expiry boundary, disabled state, unknown-user timing path, concurrent increments, and atomic failed-login audit in `backend/src/features/user-account/user-account.service.test.ts`

### Implementation for User Story 2

- [X] T025 [US2] Add account-row lock and atomic attempt/success persistence operations to `backend/src/features/user-account/user-account.repository.ts`
- [X] T026 [US2] Implement lockout state transitions so invalid attempts commit counter/lock plus canonical failed audit before returning the public error in `backend/src/features/user-account/user-account.service.ts`
- [X] T027 [US2] Verify all lockout boundaries and confirm submitted usernames/passwords never appear in unknown-user audit targets or reasons in `backend/src/features/user-account/user-account.service.test.ts`

**Checkpoint**: Lockout is concurrency-safe, observable, and does not re-enable disabled accounts.

---

## Phase 5: User Story 3 - Server-enforced scoped authorization (Priority: P1)

**Goal**: Protected services enforce self, department, branch, and all scopes using current active grants.

**Independent Test**: Execute the matrix against own, same-department, other-department, same-branch, and other-branch targets for all five roles.

### Tests for User Story 3

- [X] T028 [P] [US3] Write failing pure authorization tests for fixed role/scope mapping, multi-grant union, self without employee, malformed grants, inactive roles, and HR/Owner all-branch access in `backend/src/core/auth/authorization.test.ts`
- [X] T029 [P] [US3] Write failing request integration tests proving account disablement and role revocation take effect on the next request despite an unexpired token in `backend/src/core/auth/auth.plugin.test.ts`

### Implementation for User Story 3

- [X] T030 [US3] Implement pure target-aware authorization evaluation and privilege containment in `backend/src/core/auth/authorization.ts`
- [X] T031 [US3] Complete protected-request actor middleware that verifies token then reloads account, employee link, and active grants in `backend/src/core/auth/auth.plugin.ts`
- [X] T032 [US3] Run the five-role authorization matrix and cross-scope denial suite in `backend/src/core/auth/authorization.test.ts` and `backend/src/core/auth/auth.plugin.test.ts`

**Checkpoint**: Role revocation and account disablement are effective on the next protected action.

---

## Phase 6: User Story 4 - Account and fixed-role administration (Priority: P2)

**Goal**: HR and Owner safely administer accounts; Owner administers Owner grants; valid role scopes are enforced; the final active Owner is protected.

**Independent Test**: Create/link an account, show a temporary password once, reset/unlock/disable/enable it, grant/revoke valid scopes, reject invalid scopes/escalation, and protect the last Owner.

### Tests for User Story 4

- [X] T033 [P] [US4] Write failing account administration tests for username/employee uniqueness, one-time temporary password, reset redaction, active/disabled transitions, unlock, and final-Owner protection in `backend/src/features/user-account/user-account.admin.test.ts`
- [X] T034 [P] [US4] Write failing role tests for five-role bootstrap, no role CRUD, valid scope shapes, department-branch consistency, duplicates, inactive roles, HR-to-Owner denial, privilege escalation, revocation, and final-Owner protection in `backend/src/features/role/role.service.test.ts`
- [X] T035 [P] [US4] Write failing account/role route contract tests for IDs as decimal strings, pagination/filters, stable errors, and audit evidence in `backend/src/features/role/role.routes.test.ts`

### Implementation for User Story 4

- [X] T036 [US4] Add account list/detail/create/status/reset/unlock persistence intents and safe projections in `backend/src/features/user-account/user-account.admin.repository.ts`
- [X] T037 [US4] Implement audited account administration, secure temporary-password generation, status rules, unlock, reset, and final-Owner guard in `backend/src/features/user-account/user-account.admin.service.ts`
- [X] T038 [US4] Implement role catalog/grant repositories and organization-scope lookups in `backend/src/features/role/role.repository.ts`
- [X] T039 [US4] Implement audited grant/revoke use cases with strict scope combinations, organization validation, HR/Owner boundaries, duplicate handling, and final-Owner guard in `backend/src/features/role/role.service.ts`
- [X] T040 [US4] Implement account administration DTOs/mappers/controllers/routes in `backend/src/features/user-account/user-account.admin.dto.ts`, `backend/src/features/user-account/user-account.admin.mapper.ts`, `backend/src/features/user-account/user-account.admin.controller.ts`, and `backend/src/features/user-account/user-account.admin.routes.ts`
- [X] T041 [US4] Implement fixed-role DTOs/mappers/controllers/routes in `backend/src/features/role/role.dto.ts`, `backend/src/features/role/role.mapper.ts`, `backend/src/features/role/role.controller.ts`, and `backend/src/features/role/role.routes.ts`
- [X] T042 [US4] Run account/role service and route suites and verify that only the intended one-time response can contain a generated temporary password in `backend/src/features/user-account/*.test.ts` and `backend/src/features/role/*.test.ts`

**Checkpoint**: Account and role administration works without role CRUD or schema changes.

---

## Phase 7: User Story 5 - Complete audit observation and audit history (Priority: P1)

**Goal**: Every A1 business endpoint success/failure has exactly one correlated, redacted, append-only audit outcome; HR/Owner can inspect it.

**Independent Test**: Invoke every registered A1 action through success and applicable failure paths, then verify one canonical row, transaction rules, request correlation, append-only enforcement, and zero prohibited secrets.

### Tests for User Story 5

- [X] T043 [P] [US5] Write failing audit query authorization/filter/pagination/non-recursion route tests in `backend/src/features/audit/audit.routes.test.ts`
- [X] T044 [P] [US5] Write failing registered-action completeness test that inventories A1 routes and proves success/applicable failures have one canonical audit row in `backend/src/features/audit/audit.completeness.test.ts`
- [X] T045 [P] [US5] Write failing end-to-end secret scan over responses, captured logs, error DTOs, and serialized audit payloads in `backend/src/features/audit/audit.secret-scan.test.ts`

### Implementation for User Story 5

- [X] T046 [US5] Add scoped read-only audit query/filter persistence to `backend/src/features/audit/audit.repository.ts`
- [X] T047 [US5] Implement HR/Owner audit query service and non-recursive action observation in `backend/src/features/audit/audit.service.ts`
- [X] T048 [US5] Implement audit DTO/mapper/controller/exported routes in `backend/src/features/audit/audit.dto.ts`, `backend/src/features/audit/audit.mapper.ts`, `backend/src/features/audit/audit.controller.ts`, and `backend/src/features/audit/audit.routes.ts`
- [X] T049 [US5] Cover pre-controller validation/authentication/authorization failures through the exported transport audit plugin without observing health, preflight, static, unknown-route, or audit-insert operations in `backend/src/core/audit/a1-transport-audit.plugin.ts`
- [X] T050 [US5] Run audit atomicity, completeness, append-only, non-recursion, request-correlation, and secret-scan suites in `backend/src/core/audit/*.test.ts` and `backend/src/features/audit/*.test.ts`

**Checkpoint**: Audit coverage and redaction meet the owner's every-action requirement.

---

## Phase 8: Polish and handoff

- [X] T051 [P] Document environment variables, role/initial-Owner bootstrap, stateless logout/reset limitations, and plugin composition handoff in `backend/.env.example`, `backend/README.md`, and `specs/002-a1-auth-foundation/quickstart.md`
- [X] T052 [P] Record the department-scope trigger mismatch and forced-first-password-change limitation for the schema owner without editing migration/schema in `specs/002-a1-auth-foundation/research.md`
- [X] T053 Run `bun run typecheck` and the complete `bun test` suite from `backend/`, confirming 116 tests pass and no secret fixture is printed
- [X] T054 Review the backend diff for forbidden changes: no `backend/src/app.ts`, schema, migration, unrelated feature, frontend, or root submodule-pointer edits
- [X] T055 Execute the runnable A1 scenarios in `specs/002-a1-auth-foundation/quickstart.md` and record commands/results/known limitations in `specs/002-a1-auth-foundation/handoff.md`

---

## Dependencies and execution order

- Phase 1 blocks Phase 2.
- Phase 2 blocks all user stories because stable errors and audit are mandatory.
- US1 blocks US2 because lockout extends login.
- US1 and US2 provide authentication for US3.
- US3 blocks US4 administration authorization.
- Audit-query portions of US5 depend on US3; audit completeness depends on US1-US4.
- Polish/handoff depends on selected user stories; the complete A1 definition requires all.

```text
Setup → Foundation → US1 → US2 → US3 → US4
                       └───────────────→ US5 completeness
US1 + US2 + US3 + US4 + US5 → Polish/Handoff
```

## Parallel opportunities

- T003 and T004 may run in parallel after T001-T002.
- T005-T007 may run in parallel; implementation T008-T010 follows their failing tests.
- T015-T017 may run in parallel before US1 implementation.
- T028 and T029 may run in parallel before US3 implementation.
- T033-T035 may run in parallel before US4 implementation.
- T043-T045 may run in parallel before US5 query/completeness implementation.
- T051 and T052 may run in parallel during handoff preparation.

## Implementation strategy

1. Complete Setup and Foundation first.
2. Deliver US1 as the smallest demonstrable authentication slice.
3. Add atomic lockout, then scope authorization.
4. Add administration after the enforcement boundary is proven.
5. Close with the full audit inventory/secret scan and handoff validation.

Do not mark a task complete until its stated files exist, focused verification passes,
and no schema/migration/shared-owner file was changed outside the task contract.
