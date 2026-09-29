---
description: "Dependency-ordered A3 Employee Master and History implementation tasks"
---

# Tasks: A3 Employee Master and History

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/employee-api.md`, `quickstart.md`

**Tests**: Required by FR-023; write focused tests before each implementation slice and confirm they fail for the intended reason.

## Format

`- [ ] Tnnn [P?] [USn?] Action with exact repository-root file path`. `[P]` means independent files and no incomplete prerequisite. IDs and response money are strings; schema and migration are not edited by A3.

## Phase 1: Setup

**Purpose**: Confirm existing A1/A2 contracts and establish a test-only composition without changing Person C's `app.ts`.

- [X] T001 Record the A1 actor, audit, transaction, and A2 organization service APIs that A3 will call in `specs/004-a3-employee-history/research.md`.
- [X] T002 [P] Define A3 action names in `backend/src/core/audit/a3-transport-audit.plugin.ts`, redacted field allowlists in `backend/src/features/employee/employee.types.ts`, and safe error mapping in `backend/src/core/errors/error-codes.ts`.
- [X] T003 [P] Build an A3 test-only Elysia composition and fixtures for all five roles in `backend/src/features/employee/employee.test-support.ts`.

## Phase 2: Foundational

**Purpose**: One consistent actor/transaction/audit boundary before any user story route is exposed.

- [X] T004 Implement actor grant normalization and Owner/HR all-scope write checks in `backend/src/features/employee/employee.scope.ts`.
- [X] T005 [P] Implement canonical decimal-string ID, `YYYY-MM-DD` date, and exact `numeric(12,2)` string validators in `backend/src/features/employee/employee.validation.ts`.
- [X] T006 Register all 16 A3 public actions with one-outcome transport observation and redacted mutation facts in `backend/src/core/audit/a3-transport-audit.plugin.ts`.
- [X] T007 [P] Write tests proving all 16 action registrations, redaction, and one read/failure outcome in `backend/src/core/audit/a3-transport-audit.plugin.test.ts`.
- [X] T008 Establish shared transaction-executor and feature-service dependency interfaces in `backend/src/features/employee/employee.ports.ts`.

**Checkpoint**: A3 services can use the current actor, transactions, safe errors, and one audit outcome. No public feature behavior is delivered yet.

## Phase 3: User Story 1 — Scoped employee search and detail (P1, MVP)

**Goal**: Safe filtered employee pages and detail for Employee, Supervisor, Branch Manager, HR, and Owner.

**Independent Test**: Seed two branches/departments; verify each role's visible IDs and DTO fields, revoked access, hidden-detail not-found, and stable pagination.

- [X] T009 [P] [US1] Write five-role list/detail, hidden-resource, revoked-grant, and 1,000-row pagination tests in `backend/src/features/employee/employee.read.test.ts`.
- [X] T010 [P] [US1] Define list filters (`page`, `page_size`, `search`, `status`, `branch_id`, `department_id`) and safe response DTOs in `backend/src/features/employee/employee.dto.ts`.
- [X] T011 [US1] Implement current-assignment scoped search/count and detail queries in `backend/src/features/employee/employee.repository.ts`.
- [X] T012 [US1] Implement `listEmployees` and `getEmployee` authorization without out-of-scope existence disclosure in `backend/src/features/employee/employee.service.ts`.
- [X] T013 [US1] Implement separate team/basic, own, and HR/Owner pure response mappers with no full identity or compensation leakage in `backend/src/features/employee/employee.mapper.ts`.
- [X] T014 [US1] Add GET controller transport conversion in `backend/src/features/employee/employee.controller.ts`.
- [X] T015 [US1] Expose `GET /employees` and `GET /employees/:employee_id` with A1 authentication and A3 audit hooks in `backend/src/features/employee/employee.routes.ts`.
- [X] T016 [US1] Run US1 focused and A1/A2 regression checks, recording results in `specs/004-a3-employee-history/quickstart.md`.

**Checkpoint**: US1 works independently and is the smallest shippable A3 slice.

## Phase 4: User Story 2 — Employee identity and status (P1)

**Goal**: HR/Owner create, update, or terminate an employee without deleting history or changing account status.

**Independent Test**: Valid create/update/termination; reject duplicate code/ID, absent identity, invalid termination date, and reader mutations.

- [X] T017 [P] [US2] Write create/update/status and audit-rollback tests in `backend/src/features/employee/employee.write.test.ts`.
- [X] T018 [US2] Define create/update/status request DTOs: code ≤30 chars, national ID ≤20, passport ID ≤30, first/last names ≤100, phone ≤30, email ≤255, at least one identity in `backend/src/features/employee/employee.dto.ts`.
- [X] T019 [US2] Add insert, identity-uniqueness lookup, safe update, and status persistence in `backend/src/features/employee/employee.repository.ts`.
- [X] T020 [US2] Implement `createEmployee`, `updateEmployee`, and `changeEmployeeStatus` with HR/Owner authorization, unique-identity and hire/termination-date checks, and transactional redacted audit in `backend/src/features/employee/employee.service.ts`.
- [X] T021 [US2] Add successful create/update/status response mapping in `backend/src/features/employee/employee.mapper.ts` and `backend/src/features/employee/employee.controller.ts`.
- [X] T022 [US2] Expose POST/PATCH/PATCH-status endpoints in `backend/src/features/employee/employee.routes.ts`.

**Checkpoint**: Identity and status mutations preserve employee and account history.

## Phase 5: User Story 3 — Assignment and compensation history (P1)

**Goal**: Initial placement and effective-dated changes with exact pay and historical date lookup.

**Independent Test**: Adjacent inclusive ranges resolve correctly on each side of D; overlap, inactive org, lineage mismatch, and invalid `numeric(12,2)` values fail atomically.

- [X] T023 [P] [US3] Write boundary, overlap, organization lineage, inactive-master, exact-money, and dated-context tests in `backend/src/features/employment-assignment/employment-assignment.service.test.ts`.
- [X] T024 [US3] Add transaction-aware active Shop/Branch/Department/Position lineage validation service port in `backend/src/features/organization/organization.validation.ts`.
- [X] T025 [US3] Define assignment request/response and dated-context types with `base_salary` and `welfare_amount` as nonnegative two-decimal `numeric(12,2)` strings in `backend/src/features/employment-assignment/employment-assignment.dto.ts`.
- [X] T026 [US3] Implement assignment history, date-covered lookup, open-row lock/close, and insert queries in `backend/src/features/employment-assignment/employment-assignment.repository.ts`.
- [X] T027 [US3] Implement initial/change assignment service: validate active lineage, close old inclusive range on D-1, reject overlap/reversed range, and commit audit in one transaction in `backend/src/features/employment-assignment/employment-assignment.service.ts`.
- [X] T028 [US3] Export authorized `getEmployeeContextAtDate({ actor, employeeId, date })` from `backend/src/features/employment-assignment/employment-assignment.service.ts`.
- [X] T029 [US3] Add pure assignment response mapping and GET/POST controller in `backend/src/features/employment-assignment/employment-assignment.mapper.ts` and `backend/src/features/employment-assignment/employment-assignment.controller.ts`.
- [X] T030 [US3] Expose nested GET/POST assignment routes in `backend/src/features/employment-assignment/employment-assignment.routes.ts`.

**Checkpoint**: Historical organization and compensation facts are reproducible and usable by B/C through a service port.

## Phase 6: User Story 4 — Private bank accounts (P1; key-policy gate)

**Goal**: Encrypted account lifecycle and one-primary invariant; no full number in ordinary reads or audit.

**Independent Test**: Create two accounts, switch/deactivate primary, validate ciphertext and redaction; a failed audit rolls back mutation.

- [X] T031 [US4] Record the owner's confirmed key sourcing, version, rotation, and failure policy in `specs/004-a3-employee-history/research.md` before any bank implementation.
- [X] T032 [P] [US4] Write encryption envelope, tamper, missing-key, primary-switch, deactivate, scope, and redaction tests in `backend/src/features/employee-bank-account/employee-bank-account.service.test.ts`.
- [X] T033 [US4] Implement authenticated encryption and key-version envelope using the confirmed policy in `backend/src/features/employee-bank-account/employee-bank-account.crypto.ts`.
- [X] T034 [US4] Define account DTOs exposing only metadata and last four digits; require explicit `is_primary` on inserts despite the DBML/default mismatch in `backend/src/features/employee-bank-account/employee-bank-account.dto.ts`.
- [X] T035 [US4] Implement account lookup, insert, metadata update, current-primary lock/switch, and soft-deactivation persistence in `backend/src/features/employee-bank-account/employee-bank-account.repository.ts`.
- [X] T036 [US4] Implement authorized list/add/update/make-primary/deactivate use cases with replacement-or-explicit-no-primary and atomic redacted audit in `backend/src/features/employee-bank-account/employee-bank-account.service.ts`.
- [X] T037 [US4] Add masked mapper and transport controller in `backend/src/features/employee-bank-account/employee-bank-account.mapper.ts` and `backend/src/features/employee-bank-account/employee-bank-account.controller.ts`.
- [X] T038 [US4] Expose five nested bank-account endpoints in `backend/src/features/employee-bank-account/employee-bank-account.routes.ts`.

**Checkpoint**: Bank history and privacy hold; no bank row is persisted without authenticated encryption.

## Phase 7: User Story 5 — Weekly holiday history (P1)

**Goal**: Effective-dated weekday rules without overlapping history.

**Independent Test**: Add weekday 0 and 6, replace/end one, query old/new periods; reject -1, 7, reversal, and overlap.

- [X] T039 [P] [US5] Write weekday boundary, inclusive overlap, replacement, date-lookup, and audit-rollback tests in `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.service.test.ts`.
- [X] T040 [US5] Define weekday integer 0–6 and inclusive effective-date request/response DTOs in `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.dto.ts`.
- [X] T041 [US5] Implement history, date-covered lookup, open-row lock/close, and insert persistence in `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.repository.ts`.
- [X] T042 [US5] Implement authorized list/add-or-replace/end service with transactional redacted audit in `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.service.ts`.
- [X] T043 [US5] Add pure mapper, controller, and three nested routes in `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.mapper.ts`, `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.controller.ts`, and `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.routes.ts`.

**Checkpoint**: Historical weekly-off context remains queryable.

## Phase 8: User Story 6 — Atomic onboarding (P1)

**Goal**: Employee plus first assignment and selected bank, holidays, and account commit as one decision and one public audit fact.

**Independent Test**: Each optional step and audit failure rolls back all rows; temporary password appears only in the one-time authorized response.

- [X] T044 [P] [US6] Write all-options success, per-step rollback, one-outcome audit, and secret-exposure tests in `backend/src/features/employee/employee.onboarding.test.ts`.
- [X] T045 [US6] Add A1 internal account creation service port accepting the caller's transaction executor without independent commit or public audit in `backend/src/features/user-account/user-account.admin.service.ts`.
- [X] T046 [US6] Define nested onboarding request (`employee`, `assignment`, optional `bank_account`, `weekly_holidays[]`, `account`) and one-time credential response in `backend/src/features/employee/employee.dto.ts`.
- [X] T047 [US6] Implement `onboardEmployee` orchestration through A2/A1 and A3 feature service ports with one transaction and one redacted audit outcome in `backend/src/features/employee/employee.service.ts`.
- [X] T048 [US6] Add onboarding-only response mapper and controller in `backend/src/features/employee/employee.mapper.ts` and `backend/src/features/employee/employee.controller.ts`.
- [X] T049 [US6] Expose `POST /employees/onboard` in `backend/src/features/employee/employee.routes.ts`.

**Checkpoint**: No partial onboarding state or secret leak remains after any failure.

## Phase 9: Polish and cross-cutting verification

- [X] T050 [P] Export one independently composable A3 route bundle without editing `app.ts` in `backend/src/features/employee/employee.routes.ts`.
- [X] T051 [P] Add a 16-action audit matrix and failure rollback regression test in `backend/src/features/employee/employee.audit.test.ts`.
- [X] T052 Run `bun run typecheck` and `bun test` in `backend/`; run each database integration file in an isolated migrated PostgreSQL database and record pass/skip counts in `specs/004-a3-employee-history/quickstart.md`.
- [X] T053 Reconcile `spec.md`, `plan.md`, `tasks.md`, and `contracts/employee-api.md` against implemented behavior and note schema-owner bank-default follow-up in `specs/004-a3-employee-history/quickstart.md`.

## Dependencies and execution order

`Setup → Foundational → US1 → US2 → US3 → (US4, US5 in parallel) → US6 → Polish`. US4 additionally waits for the bank key-policy answer (T031). US2 can start after Foundational, but its employee repository should be integrated after US1 to avoid same-file conflicts. US5 can start after US3's employee/transaction context. US6 requires all selected components, including US4 when a bank is selected. T045 must be an A1 service port, not an A1 repository import from A3.

## Parallel examples

- US1: T009 and T010 can proceed in separate files; T011 then T012–T015 are sequential integrations.
- US3: T023 and A2 validation work T024 can proceed independently before service integration.
- US4/US5: after US3 and T031, separate feature owners can implement each lifecycle without file overlap.
- US6: T044 tests and T045 A1 internal service port can proceed independently before onboarding orchestration.

## Implementation strategy

Deliver US1 as MVP and validate its scope/field matrix. Then add identity, dated assignment context, bank and holiday lifecycles, and finally atomic onboarding. Keep schema/migrations and `backend/src/app.ts` untouched; pass Person C the route bundle and B/C the dated-context service API. Stop bank-inclusive work until T031 is resolved.
