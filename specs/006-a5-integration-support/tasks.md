# Tasks: A5 Integration Support

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/employee-context.md.

## Phase 1: Setup

- [X] T001 Inventory A1–A4, attendance, payroll, and audit coverage in specs/006-a5-integration-support/research.md.
- [X] T002 Freeze dated context contract in specs/006-a5-integration-support/contracts/employee-context.md.

## Phase 2: US1 — Historical context

**Independent test**: Transfer/pay fixtures resolve on both sides of effective dates.

- [X] T003 [US1] Add historical context and attendance visibility tests in backend/src/features/employee/employee.a5-integration.test.ts.
- [X] T004 [US1] Verify payroll daily compensation boundary in backend/src/features/payroll/calculation/payroll-calculator.test.ts and backend/src/features/payroll/payroll.input-projection.test.ts.
- [X] T005 [US1] Correct missing-row return type in backend/src/features/employee/employee.operation-context.repository.ts and document the fix in specs/006-a5-integration-support/quickstart.md.

## Phase 3: US2 — Authorization and audit

**Independent test**: Five roles, historical scopes, and audit actions pass without a live database.

- [X] T006 [P] [US2] Add five-role authorization matrix in backend/src/features/employee/employee.a5-integration.test.ts.
- [X] T007 [P] [US2] Add A1–A3 audit completeness, redaction, and malformed-ID tests in backend/src/features/audit/a5-audit-matrix.test.ts and fix A1/A2 transport fallback in backend/src/core/audit/.
- [X] T008 [US2] Remove plaintext fixture-password output in backend/src/test/b5-operations-journey.test.ts and document the fix in specs/006-a5-integration-support/quickstart.md.

## Phase 4: US3 — Demo handoff

**Independent test**: Commands/results reproduce checks.

- [X] T009 [US3] Rehearse login → employee → history in backend/src/test/a5-identity-hr-journey.test.ts and record results in specs/006-a5-integration-support/quickstart.md.
- [X] T010 [US3] Run backend typecheck/tests and frontend tests/lint/build; record outcomes in specs/006-a5-integration-support/quickstart.md.
- [X] T011 [US3] Summarize Person C demo dependencies and fixes in specs/006-a5-integration-support/quickstart.md.

## Dependencies

Setup → US1 and US2 (parallel after inventory) → US3. T005/T008 conditional on defects.

## Implementation Strategy
