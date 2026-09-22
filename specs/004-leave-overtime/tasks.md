# Tasks: Leave and Overtime

**Input**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), and [contract](contracts/leave-overtime-api.md)

**Tests**: Required. Write focused Bun service tests before each implementation slice.

## Phase 1: Foundations

- [X] T001 Define injected actor scope, unit-of-work, attendance-effect, and payroll-lock interfaces in `backend/src/features/leave/leave.service.ts` and `backend/src/features/overtime/overtime.service.ts`.
- [X] T002 Define stable B2 errors and DTO/mapper contracts in `backend/src/features/leave/leave.dto.ts`, `backend/src/features/leave/leave.mapper.ts`, `backend/src/features/overtime/overtime.dto.ts`, and `backend/src/features/overtime/overtime.mapper.ts`.

## Phase 2: User Story 1 - Submit and approve leave (P1)

**Independent Test**: Submit two days, approve as a supervisor, and verify quota,
attendance, and history effects occur together.

- [X] T003 [US1] Write failing leave tests for pending/approved overlap, quota exact/exceeded, supervisor three-day approval, manager direct approval, scope denial, and rollback in `backend/src/features/leave/leave.test.ts`.
- [X] T004 [US1] Implement frozen-table persistence, employee serialization, and stable overlap/quota conflicts in `backend/src/features/leave/leave.repository.ts`.
- [X] T005 [US1] Implement pending submission and transactional approval including quota locking and attendance-effect adapter in `backend/src/features/leave/leave.service.ts`.
- [X] T006 [US1] Implement validation, response mapping, and exported unmounted leave request routes in `backend/src/features/leave/leave.controller.ts` and `backend/src/features/leave/leave.routes.ts`.

## Phase 3: User Story 2 - Preserve leave decisions (P2)

**Independent Test**: Approve with a corrected type and confirm original/final types
and immutable ordered history; reject another request with no quota effect.

- [X] T007 [US2] Add failing tests for type correction, already-decided conflict, rejection without effects, frozen quota, and append-only actions in `backend/src/features/leave/leave.test.ts`.
- [X] T008 [US2] Implement final-type validation, rejection, and append-only decision history in `backend/src/features/leave/leave.service.ts` and `backend/src/features/leave/leave.repository.ts`.
- [X] T009 [US2] Extend leave DTO mapping and route decisions in `backend/src/features/leave/leave.dto.ts`, `backend/src/features/leave/leave.mapper.ts`, `backend/src/features/leave/leave.controller.ts`, and `backend/src/features/leave/leave.routes.ts`.

## Phase 4: User Story 3 - Explicit overtime approval (P3)

**Independent Test**: Submit all three OT types, approve one, and ensure only that
one appears in payroll reads.

- [X] T010 [US3] Write failing OT tests for each type/value combination, qualifying context, duplicate date, state conflict, scope denial, and approved-only payroll reads in `backend/src/features/overtime/overtime.test.ts`.
- [X] T011 [US3] Implement frozen-table persistence and unique/conflict translation in `backend/src/features/overtime/overtime.repository.ts`.
- [X] T012 [US3] Implement transactional submit, explicit approve/reject, context validation, and approved payroll range reader in `backend/src/features/overtime/overtime.service.ts`.
- [X] T013 [US3] Implement validation, response mapping, and exported unmounted OT routes in `backend/src/features/overtime/overtime.dto.ts`, `backend/src/features/overtime/overtime.mapper.ts`, `backend/src/features/overtime/overtime.controller.ts`, and `backend/src/features/overtime/overtime.routes.ts`.

## Phase 5: Validation and handoff

- [X] T014 Run typecheck, leave/OT tests, and opt-in PostgreSQL fixture tests from `specs/004-leave-overtime/quickstart.md`.
- [X] T015 Document Person A/C adapters, approved payroll readers, pending-overlap concurrency protection, and the frozen `draft`/`pending` schema discrepancy in `specs/004-leave-overtime/contracts/leave-overtime-api.md`.

## Dependencies and execution order

`T001–T002 → US1 → US2 → US3 → T014–T015`.

US2 extends the leave workflow from US1. US3 can begin after foundations but is
scheduled after leave for focused review. Person C must provide composition,
transactions, payroll locks, and error mapping; Person A supplies scope and
effective-assignment adapters.

## MVP

User Story 1 is the MVP: transactional leave submission and approval with the
three-day supervisor boundary.
