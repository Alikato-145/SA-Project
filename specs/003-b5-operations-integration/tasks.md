# Tasks: B5 Operations and Payroll Integration

**Input**: [plan.md](plan.md), [spec.md](spec.md), research.md, data-model.md, contracts/operations.md
**Tests**: Required by acceptance outcomes and project constitution. Checklists are requirements quality only.

## Phase 1: Setup

- [X] T001 Inspect clean submodule state, install locked dependencies in backend/package.json and frontend/package.json, verify ignore files and provision disposable PostgreSQL using compose.yaml; record baseline in specs/003-b5-operations-integration/validation.md.

## Phase 2: Foundational

- [X] T002 Implement historical employee/scope context service and owning persistence adapters in backend/src/features/employee/ and backend/src/features/attendance/; match permission/scope from same trusted grant, including multi-grant actors (FR-002, FR-003).
- [X] T003 Implement payroll service/repository transaction-aware mutation guards and advance projection in backend/src/features/payroll/payroll.service.ts and payroll.repository.ts; serialize operational mutations with final projection (FR-008, FR-011, FR-012).
- [X] T004 Integrate authenticated transport, origin/request validation, stable public errors, controller envelopes, mapper conversion and transactional audit adapters across backend/src/features/{branch-schedule,holiday-calendar,attendance,leave,overtime,advance,loan,debt}/; public IDs use "positive decimal string, converted only when safely representable by current persistence mapping", money uses "decimal string; never floating-point arithmetic", dates use "real ISO YYYY-MM-DD date" (FR-002–004, FR-013).
- [X] T005 [P] Add shared typed operation requests, session/error handling and public types in frontend/lib/operations/operations-api.ts and operations-api.test.ts (FR-004).

## Phase 3: US1 — Signed-in operations (P1, MVP)

**Independent test**: Authorized schedule/holiday/attendance save and read-back, historical transfer and scope rejection.

- [X] T006 [US1] Add runtime scope, validation, transfer and schedule/holiday regression checks in backend/src/features/attendance/attendance.test.ts and backend/src/features/branch-schedule/branch-schedule.test.ts (FR-001–005).
- [X] T007 [US1] Wire safe attendance/schedule/holiday services and plugins in backend/src/app.ts; derive/validate dated schedule context, preserve successor schedule history and locked facts in backend/src/features/{attendance,branch-schedule,holiday-calendar}/ (FR-001, FR-005, FR-012, FR-013).
- [X] T008 [US1] Integrate attendance/schedule/override/holiday controls and string identifiers in frontend/app/(dashboard)/attendance/page.tsx; enable operations in frontend/lib/auth/route-access.ts and frontend/components/application-shell.tsx (FR-001, FR-004).

## Phase 4: US2 — Leave and OT (P1)

**Independent test**: Submit/decide leave and all OT types, inspect quota/history/attendance; verify 3/4-day and transactional rejection cases.

- [X] T009 [US2] Extend backend/src/features/leave/leave.test.ts and backend/src/features/overtime/overtime.test.ts for matching-grant authority, atomic failures, approved leave non-deduction and real OT eligibility (FR-006, FR-007).
- [X] T010 [US2] Integrate leave and OT services, quota/type/history reads, payroll guards and dated eligibility in backend/src/features/{leave,overtime,attendance}/ and backend/src/app.ts (FR-001, FR-006, FR-007, FR-013).
- [X] T011 [US2] Integrate shared client, self/approver state, type/quota/history display in frontend/app/(dashboard)/leave/page.tsx and frontend/app/(dashboard)/overtime/page.tsx (FR-001, FR-004, FR-006, FR-007).

## Phase 5: US3 — Finance (P1)

**Independent test**: Advance boundaries, exact loan installments, debt/reversal and deductions reconcile to sources.

- [X] T012 [US3] Add configured advance and atomic decision regressions in backend/src/features/advance/advance.test.ts plus finance projection regressions in backend/src/features/payroll/payroll.projection.integration.test.ts (FR-008–011).
- [X] T013 [US3] Integrate transaction-scoped advance eligibility/projection/configuration, loan and debt runtime and audit in backend/src/features/{advance,loan,debt}/ and backend/src/app.ts (FR-001, FR-008, FR-009, FR-013).
- [X] T014 [US3] Integrate exact-ID finance requests, ledger/reversal and decision feedback in frontend/app/(dashboard)/finance/page.tsx (FR-001, FR-004, FR-009).

## Phase 6: US4 — Payroll handoff (P2)

**Independent test**: Disposable two-branch journey through payroll lock and protected correction attempts; exact expected totals and repeated settlement rejection.

- [X] T015 [US4] Correct shop-specific inputs/pending checks, exclude reversed originals, prevent approved leave deductions, preserve atomic settlement and lock in backend/src/features/payroll/payroll.repository.ts and calculation/payroll-calculator.ts with focused regressions (FR-010–012).
- [X] T016 [US4] Add repeatable real-database operations-to-payroll journey and concurrency/rollback cases in backend/src/test/b5-operations-journey.test.ts (FR-001–014, SC-001–006).

## Phase 7: Validation and handoff

- [X] T017 Run backend typecheck/full tests with disposable database and frontend tests/lint/build; perform running UI walkthrough; record observed commands, outcomes, limitations and reproducibility instructions in specs/003-b5-operations-integration/validation.md and quickstart.md (FR-014, SC-001–006).

## Dependencies & Execution Order

Setup → foundations → story implementations → integrated journey → final validation. T002/T003 lock/context interfaces must be agreed before feature wiring. T005 is independent frontend client work after contract design. US1/US2/US3 can be implemented by feature owners after foundations, but edits to app.ts are serialized. US4 final validation depends on all three; payroll projection implementation can proceed alongside B feature wiring after T003. No schema/migration or root submodule pointer updates.

## Parallel Examples

US1: frontend attendance controls and backend attendance tests use separate files. US2: leave and OT checks can be authored separately after shared contracts. US3: frontend finance integration and backend projection regressions are independent. US4: fixture preparation and payroll calculator regressions use separate files, then execute together. Shared files and API-shape changes are coordinated before parallel implementation.

## Implementation Strategy

Deliver signed-in attendance as MVP; then leave/OT and finance; finally integrated payroll lock. Tests precede changed logic where meaningful. Reuse existing feature services and test helpers, keep repositories feature-owned and mappers controller-only. Mark completion only after work and evidence exist; do not mark database skips as passing.
