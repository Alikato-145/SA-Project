# Tasks: Operations and Finance Screens

**Input**: [spec.md](spec.md), [plan.md](plan.md), [API contract](contracts/ui-api.md)

## Phase 1: Setup

- [X] T001 Confirm B1–B3 API field names and Next 16 client-page guidance in `specs/006-operations-finance-ui/research.md`.

## Phase 2: Attendance (US1)

**Goal**: Review and enter scoped work-day records.
**Independent Test**: List, submit, correct, and see fresh data or a business error.

- [X] T002 [US1] Implement employee/date filters, record list, loading/empty/error states in `frontend/app/(dashboard)/attendance/page.tsx`.
- [X] T003 [US1] Add manual entry and permitted correction controls in `frontend/app/(dashboard)/attendance/page.tsx`.

## Phase 3: Leave and overtime (US2)

**Goal**: Submit and decide leave and OT requests.
**Independent Test**: Each page independently shows a pending request and its final decision.

- [X] T004 [US2] Implement request/list/decision flows in `frontend/app/(dashboard)/leave/page.tsx`.
- [X] T005 [US2] Implement three-type request/list/decision flows in `frontend/app/(dashboard)/overtime/page.tsx`.

## Phase 4: Finance (US3)

**Goal**: Submit and review advances, loans, and debt.
**Independent Test**: Each finance section refreshes after a successful write.

- [X] T006 [US3] Implement advance request/list/decision in `frontend/app/(dashboard)/finance/page.tsx`.
- [X] T007 [US3] Implement loan create/list/installment schedule in `frontend/app/(dashboard)/finance/page.tsx`.
- [X] T008 [US3] Implement debt record/list/reversal and balance in `frontend/app/(dashboard)/finance/page.tsx`.

## Phase 5: Validation and handoff

- [X] T009 Run frontend lint and build; record results in `specs/006-operations-finance-ui/quickstart.md`.
- [X] T010 Record Person C's mount, navigation, and proxy requirements in `specs/006-operations-finance-ui/contracts/ui-api.md`.

## Dependencies

`T001 → T002–T003 → T004–T005 → T006–T008 → T009–T010`.
