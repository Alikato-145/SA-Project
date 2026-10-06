# Tasks: Employee Finance

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [API contract](contracts/finance-api.md)

**Tests**: Focused Bun service checks and opt-in PostgreSQL constraints.

## Phase 1: Setup

- [X] T001 Confirm frozen finance table constraints and adapter contracts in `specs/005-employee-finance/contracts/finance-api.md`.

## Phase 2: Foundational

- [X] T002 Define exact cent conversion and allocation behavior in `backend/src/features/loan/loan.service.ts` and `backend/src/features/loan/loan.test.ts`.

## Phase 3: User Story 1 - Advance eligibility (P1)

**Goal**: Submit and decide one advance per employee/month.

**Independent Test**: Day 19/20, worked days 19/20, half salary, and projected
net pay boundaries.

- [X] T003 [US1] Add failing boundary tests in `backend/src/features/advance/advance.test.ts`.
- [X] T004 [US1] Implement exact amount validation, effective context checks, and approval/rejection rules in `backend/src/features/advance/advance.service.ts`.
- [X] T005 [US1] Implement frozen-table persistence, unique-month conflict, and approved payroll reader in `backend/src/features/advance/advance.repository.ts`.
- [X] T006 [US1] Export validated, unmounted request/decision routes and safe response mapping in `backend/src/features/advance/advance.routes.ts`, `backend/src/features/advance/advance.controller.ts`, `backend/src/features/advance/advance.dto.ts`, and `backend/src/features/advance/advance.mapper.ts`.

## Phase 4: User Story 2 - Loan installments (P2)

**Goal**: Create an exact one-to-five-month schedule and expose due items to
payroll; only payroll lock can mark an installment deducted.

**Independent Test**: Non-divisible principal sums exactly and a settlement
retry cannot deduct twice.

- [X] T007 [US2] Add failing cent allocation and settlement-state tests in `backend/src/features/loan/loan.test.ts`.
- [X] T008 [US2] Implement loan and installment transaction, due-reader, and conditional settlement in `backend/src/features/loan/loan.repository.ts`.
- [X] T009 [US2] Implement authorized create, exact schedule, and payroll-lock settlement service in `backend/src/features/loan/loan.service.ts`.
- [X] T010 [US2] Export validated, unmounted loan routes and safe DTO mapping in `backend/src/features/loan/loan.routes.ts`, `backend/src/features/loan/loan.controller.ts`, `backend/src/features/loan/loan.dto.ts`, and `backend/src/features/loan/loan.mapper.ts`.

## Phase 5: User Story 3 - Append-only debt ledger (P3)

**Goal**: Record scoped charges and adjustments, reverse once, and derive balance.

**Independent Test**: A charge and its reversal both remain visible; a second
reversal or settled target is rejected.

- [X] T011 [US3] Add failing ledger and reversal tests in `backend/src/features/debt/debt.test.ts`.
- [X] T012 [US3] Implement insert-only transaction persistence, reversal locking, and ledger reader in `backend/src/features/debt/debt.repository.ts`.
- [X] T013 [US3] Implement scoped charge, adjustment, reversal, and signed balance service in `backend/src/features/debt/debt.service.ts`.
- [X] T014 [US3] Export validated, unmounted debt routes and safe DTO mapping in `backend/src/features/debt/debt.routes.ts`, `backend/src/features/debt/debt.controller.ts`, `backend/src/features/debt/debt.dto.ts`, and `backend/src/features/debt/debt.mapper.ts`.

## Phase 6: Polish and handoff

- [X] T015 Run package typecheck/tests and document results in `specs/005-employee-finance/quickstart.md`.
- [X] T016 Report the frozen debt settlement conflict and payroll source-link option in `specs/005-employee-finance/contracts/finance-api.md`.

## Dependencies

`T001–T002 → US1 → US2 → US3 → T015–T016`. US1 is the MVP. The three feature
folders do not overlap, so their tests and DTOs can be prepared independently;
decision and persistence changes in the same file remain sequential. Person C
owns route composition, projected pay, payroll lock, and debt settlement choice.
