# Tasks: Schedules and Attendance

**Input**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), [API contract](contracts/attendance-api.md), and
[integration contract](contracts/integration.md)

**Tests**: Required. Write focused Bun tests before implementation. PostgreSQL tests
use a disposable `TEST_DATABASE_URL` and rollback-only fixtures.

**Execution control**: This work is split into three sequential main phases to
control conversation token use. Execute only one main phase per user request. At
each stop point, report changed files, test results, and blockers; do not begin the
next main phase until the user asks. No phase changes schema, migrations, shared app
files, or frontend code.

## Shared prerequisite

Before Phase 1 begins, Person B records the agreed actor/scope,
effective-assignment, error-boundary, route-composition, and payroll-lock interfaces
in `specs/003-schedules-attendance/contracts/integration.md`. This is coordination,
not a fourth implementation phase.

---

## Main Phase 1: Branch Schedules and Overrides

**Goal**: An authorized manager can maintain normal schedules and date-specific
exceptions, and consumers can resolve the applicable outcome.

**Independent Test**: Create a schedule, resolve it within range, add an override,
and verify that the override takes precedence; ranges sharing an end/start date
must conflict.

- [X] T001 [P] [US1] Create schedule DTOs, mapper types, repository interface, service dependencies, and stable B1 errors in `backend/src/features/branch-schedule/branch-schedule.dto.ts`, `backend/src/features/branch-schedule/branch-schedule.mapper.ts`, `backend/src/features/branch-schedule/branch-schedule.repository.ts`, and `backend/src/features/branch-schedule/branch-schedule.service.ts`.
- [X] T002 [US1] Write failing service tests for scope denial before persistence, inclusive ranges, non-negative grace, `SCHEDULE_RANGE_OVERLAP`, no-schedule, and override precedence in `backend/src/features/branch-schedule/branch-schedule.test.ts`.
- [X] T003 [US1] Write failing override tests for unique `(branch_id, schedule_date)`, closed overrides without hours, complete open overrides, and `INVALID_OVERRIDE_HOURS` in `backend/src/features/branch-schedule/branch-schedule.test.ts`.
- [X] T004 [US1] Implement persistence using frozen `branchSchedules` and `branchScheduleOverrides`, translating unique/check/exclusion failures to stable errors in `backend/src/features/branch-schedule/branch-schedule.repository.ts`.
- [X] T005 [US1] Implement create, update, applicable-schedule resolution, and override upsert in `backend/src/features/branch-schedule/branch-schedule.service.ts`; an applicable override must precede the effective normal schedule.
- [X] T006 [US1] Implement validation, response mapping, and exported unmounted routes in `backend/src/features/branch-schedule/branch-schedule.controller.ts` and `backend/src/features/branch-schedule/branch-schedule.routes.ts`.

**Stop point**: Report the exported schedule-route surface and test results. Do not
start Main Phase 2 until the user asks.

---

## Main Phase 2: Holiday Calendar

**Goal**: An authorized manager can record, find, and deactivate a shop holiday.

**Independent Test**: Create an active holiday, find it for its shop/date,
deactivate it, and verify active-only lookup omits it.

- [X] T007 [P] [US2] Create holiday DTOs, mapper types, repository interface, service dependencies, and stable B1 errors in `backend/src/features/holiday-calendar/holiday-calendar.dto.ts`, `backend/src/features/holiday-calendar/holiday-calendar.mapper.ts`, `backend/src/features/holiday-calendar/holiday-calendar.repository.ts`, and `backend/src/features/holiday-calendar/holiday-calendar.service.ts`.
- [X] T008 [US2] Write failing service tests for actor scope, active-only lookup, duplicate `(shop_id, holiday_date)` conflict, and deactivation in `backend/src/features/holiday-calendar/holiday-calendar.test.ts`.
- [X] T009 [US2] Implement persistence and duplicate-conflict translation using frozen `holidayCalendars` in `backend/src/features/holiday-calendar/holiday-calendar.repository.ts`.
- [X] T010 [US2] Implement create, list, active lookup, and deactivate use cases in `backend/src/features/holiday-calendar/holiday-calendar.service.ts`.
- [X] T011 [US2] Implement validation, response mapping, and exported unmounted routes in `backend/src/features/holiday-calendar/holiday-calendar.controller.ts` and `backend/src/features/holiday-calendar/holiday-calendar.routes.ts`.

**Stop point**: Report the holiday API surface and test results. Do not start Main
Phase 3 until the user asks.

---

## Main Phase 3: Manual Attendance and Handoff

**Goal**: An authorized manager records one employee/date with a historical branch
snapshot and corrects allowed fields before payroll locks.

**Independent Test**: Create one manual record, verify its branch/source, reject a
duplicate and inverted timestamps, correct the existing record, then read it by date
range without changing its branch.

- [X] T012 [P] [US3] Create attendance DTOs, mapper types, repository interface, service dependencies, and stable B1 errors in `backend/src/features/attendance/attendance.dto.ts`, `backend/src/features/attendance/attendance.mapper.ts`, `backend/src/features/attendance/attendance.repository.ts`, and `backend/src/features/attendance/attendance.service.ts`.
- [X] T013 [US3] Write failing service tests for effective-assignment scope checks, manual source assignment, duplicate conflict, clock order, historical branch retention, date-range reads, and payroll-lock rejection in `backend/src/features/attendance/attendance.test.ts`.
- [X] T014 [US3] Add opt-in database tests for work-day uniqueness, clock ordering, and stored branch snapshot in `backend/src/features/attendance/attendance.test.ts` using `TEST_DATABASE_URL` and rollback-only fixtures.
- [X] T015 [US3] Implement persistence, correction without branch/source mutation, date-range payroll reads, and database conflict translation using frozen `workDayRecords` in `backend/src/features/attendance/attendance.repository.ts`.
- [X] T016 [US3] Implement manual create, correction, read-range, effective-date scope validation, and payroll-lock guard use cases in `backend/src/features/attendance/attendance.service.ts`.
- [X] T017 [US3] Implement validation, response mapping, and exported unmounted routes in `backend/src/features/attendance/attendance.controller.ts` and `backend/src/features/attendance/attendance.routes.ts`.
- [X] T018 [US3] Run B1 typecheck, feature tests, opt-in database tests, and manual validation from `specs/003-schedules-attendance/quickstart.md`.
- [X] T019 [US3] Update Person C handoff with route names, error codes, payroll range-reader fields, and remaining dependency limits in `specs/003-schedules-attendance/contracts/integration.md`.

**Stop point**: Report all B1 integration handoff details, validation results, and
any remaining Person A/C blockers. B1 is then ready for review.

---

## Dependencies and execution order

```text
Person A/C contract confirmation
      ↓
Main Phase 1: schedules and overrides
      ↓ user-requested stop point
Main Phase 2: holiday calendar
      ↓ user-requested stop point
Main Phase 3: manual attendance
      ↓
Person C route composition and payroll integration
```

- The source paths for the three phases do not overlap. Phase 2 is technically
  independent after the shared prerequisite, but remains sequential by choice so
  work can be reviewed in small requests.
- Phase 3 requires Person A's effective-assignment lookup and Person C's payroll
  lock guard for complete correction behavior. Its local tests can begin with fakes.
- Every phase exports routes only; Person C owns route composition in `app.ts`.

## Current Status

All B1 implementation tasks are complete. Route composition and runtime adapters
remain Person C and Person A integration work.
