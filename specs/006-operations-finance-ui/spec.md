# Feature Specification: Operations and Finance Screens

**Feature Branch**: `main`

**Created**: 2026-09-22

**Status**: Draft

**Input**: Implement Person B work package B4 from `docs/two-week-three-person-plan.md` within owned frontend routes.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Review and enter attendance (Priority: P1)

An authorized operator selects an employee and date range, reviews work-day records, and enters a manual record or correction.

**Why this priority**: Payroll depends on accurate attendance.

**Independent Test**: With a reachable API, an operator can list and submit a manual work day and see the result without leaving the screen.

**Acceptance Scenarios**:

1. **Given** an employee and date range, **When** the operator loads attendance, **Then** matching records and their historical branch are visible.
2. **Given** a valid manual record, **When** it is submitted, **Then** the server response is shown and the list refreshes.

---

### User Story 2 - Request and decide leave or overtime (Priority: P2)

An employee or scoped manager reviews leave and OT, submits requests, and an authorized approver records a decision.

**Why this priority**: These decisions change attendance and payable OT.

**Independent Test**: A leave or OT request appears pending; an approval or rejection changes its displayed state.

**Acceptance Scenarios**:

1. **Given** a valid request, **When** it is submitted, **Then** the pending record appears with its dates and type.
2. **Given** a pending request, **When** a scoped approver decides it, **Then** the decision state appears or a clear business error is shown.

---

### User Story 3 - Manage employee finance (Priority: P3)

An authorized user reviews and records advances, loans, and debt entries from one finance area.

**Why this priority**: The payroll demo requires these inputs before lock.

**Independent Test**: Submit each finance type, review its list, and use the allowed advance and debt decisions.

**Acceptance Scenarios**:

1. **Given** an eligible request, **When** an advance is submitted or decided, **Then** the latest status is visible.
2. **Given** a loan, **When** it is created, **Then** the installment schedule is visible.
3. **Given** a debt transaction, **When** it is recorded or reversed, **Then** the ledger and balance refresh.

### Edge Cases

- An empty list shows a useful message; loading and server errors are distinguishable.
- The server denies an out-of-scope action or a conflicting historical change.
- Monetary input retains two-decimal precision; missing required fields block submission.
- A request succeeds but the follow-up list fails: success remains visible, with a refresh error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to filter and read attendance, leave, OT, and finance records for a selected employee.
- **FR-002**: Authorized operators MUST be able to submit manual attendance and correct a permitted record.
- **FR-003**: Users MUST be able to submit leave and OT requests and send approval/rejection decisions.
- **FR-004**: Users MUST be able to submit and decide advances, create loans, and record/reverse debt transactions.
- **FR-005**: Every screen MUST communicate loading, empty, success, validation, and server-error states in plain language.
- **FR-006**: A successful mutation MUST refresh the relevant list without requiring full-page navigation.
- **FR-007**: The screens MUST preserve the server's authorization and business decisions; disabled controls alone cannot grant access.
- **FR-008**: Pages MUST work with keyboard input and labelled controls at desktop and mobile widths.

### Key Entities *(include if feature involves data)*

- **Work-day record**: Employee, historical branch, date, status, times, deduction.
- **Leave/OT request**: Employee, requested dates/type, amount, status.
- **Advance/loan/debt**: Requested amount and status; installment schedule; immutable ledger entries.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All six Person B workflows can be reached from the four owned routes.
- **SC-002**: In a scripted demo, a user can submit each request and see its resulting state without a reload.
- **SC-003**: All tested API validation and state-conflict responses appear as understandable page messages.
- **SC-004**: Frontend lint and production build pass.

## Assumptions

- Person C owns the shared dashboard layout, navigation, API client, session handling, and route composition. These pages use relative `/api` paths and await that integration.
- The backend remains authoritative for access checks and business rules.
- Backend IDs and decimal amounts use the existing package contracts; no frontend database access is added.
