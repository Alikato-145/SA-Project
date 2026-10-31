# Tasks: Person B Payroll Handoff

**Input**: [spec.md](spec.md), [plan.md](plan.md), [handoff contract](contracts/person-c-handoff.md)

## Phase 1: Setup

- [X] T001 Confirm B1–B3 reader/filter contracts and frozen table behavior in `specs/007-person-b-payroll-handoff/research.md`.

## Phase 2: Approved leave attendance (US1)

**Goal**: Apply leave to attendance inside the approval transaction.
**Independent Test**: Existing absence updates, missing record gets historical branch, conflicting worked day rejects.

- [X] T002 [US1] Add focused effect tests in `backend/src/features/attendance/attendance-leave-effect.test.ts`.
- [X] T003 [US1] Implement transaction-scoped work-day read/write in `backend/src/features/attendance/attendance-leave-effect.repository.ts`.
- [X] T004 [US1] Implement leave effect and historical branch contract in `backend/src/features/attendance/attendance-leave-effect.service.ts`.

## Phase 3: Advance worked days (US2)

**Goal**: Count accepted present/late days in a bounded month.
**Independent Test**: 19 vs 20 days and nonworked statuses.

- [X] T005 [US2] Add worked-day tests in `backend/src/features/attendance/attendance.test.ts`.
- [X] T006 [US2] Add attendance count/advance adapter in `backend/src/features/attendance/attendance.service.ts`.

## Phase 4: Payroll handoff (US3)

**Goal**: Give C explicit reader and blocking-decision contracts.
**Independent Test**: Reader filters and handoff are inspectable, backed by focused tests.

- [X] T007 [US3] Verify approved/due/candidate readers and record C handoff in `specs/007-person-b-payroll-handoff/contracts/person-c-handoff.md`.
- [X] T008 Run backend typecheck/test and record validation in `specs/007-person-b-payroll-handoff/quickstart.md`.

## Dependencies

`T001 → T002–T004 → T005–T006 → T007–T008`.
