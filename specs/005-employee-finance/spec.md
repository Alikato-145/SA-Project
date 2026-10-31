# Feature Specification: Employee Finance

**Feature Branch**: `main`

**Created**: 2026-09-22

**Status**: Draft

**Input**: Implement Person B work package B3, advances, loans, and debt, from `docs/two-week-three-person-plan.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Request and approve an advance (Priority: P1)

An employee requests an advance for a month, and an authorized manager decides it
after checking eligibility and the resulting pay.

**Why this priority**: An advance can affect the next payroll and must not leave
the employee with negative net pay.

**Independent Test**: Submit one request on or after the 20th with at least 20
worked days and an amount at or below half of base salary; approve it only when
the projected net pay remains non-negative.

**Acceptance Scenarios**:

1. **Given** an eligible employee, **When** the employee requests an amount
   within the cap, **Then** one pending request exists for that month.
2. **Given** a pending request, **When** an authorized manager approves it,
   **Then** all eligibility checks are repeated against current facts and the
   decision is recorded.
3. **Given** any failed eligibility check, **When** approval is attempted,
   **Then** no deduction is committed and the reason is visible.

---

### User Story 2 - Manage loan installments (Priority: P2)

An authorized manager records a loan with one to five monthly installments;
payroll deducts each scheduled installment once when its period locks.

**Why this priority**: Repayment must be traceable to the loan and payroll period.

**Independent Test**: Create a loan with three installments, verify their amounts
sum to the principal, and mark one installment deducted only with a payroll lock.

**Acceptance Scenarios**:

1. **Given** a valid principal and one-to-five installment count, **When** a
   manager approves a loan, **Then** a dated repayment schedule is visible.
2. **Given** a scheduled installment, **When** payroll locks the due period,
   **Then** it is linked to that payroll record and marked deducted once.

---

### User Story 3 - Preserve debt transactions (Priority: P3)

An authorized finance user records charges, adjustments, and reversals while
retaining every original transaction.

**Why this priority**: Food and other employee debt history must be auditable.

**Independent Test**: Record a charge, reverse it, and confirm both entries
remain visible and the calculated balance is zero.

**Acceptance Scenarios**:

1. **Given** an active debt type, **When** a scoped finance user records a
   positive charge, **Then** it appears in the employee ledger.
2. **Given** an unsettled charge, **When** it is reversed, **Then** a new linked
   reversal appears and the original remains unchanged.
3. **Given** a settled transaction, **When** reversal is requested, **Then** the
   operation is denied and the payroll adjustment path is required.

### Edge Cases

- The advance request is on the 19th versus the 20th.
- The employee has 19 versus 20 worked days.
- The advance is exactly half of base salary, one cent above it, or would make
  projected net pay negative.
- A second advance is submitted for the same employee and month.
- A loan has one or five installments, an invalid sixth, or a non-divisible
  principal that requires cent allocation.
- A payroll retry attempts to deduct the same installment twice.
- A debt reversal is submitted twice, or targets another employee's transaction.
- An out-of-scope actor tries to view or change another employee's finance data.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST permit at most one advance request per employee
  and month.
- **FR-002**: The system MUST require a request date on or after the 20th and at
  least 20 worked days before advance approval.
- **FR-003**: The system MUST cap an advance at half of base salary and deny an
  approval that would make net pay negative after deductions.
- **FR-004**: The system MUST record the actor, time, outcome, and reason for
  each advance decision without rewriting an approved deduction.
- **FR-005**: The system MUST create one to five dated loan installments whose
  exact amounts sum to the principal.
- **FR-006**: The system MUST mark an installment deducted at most once and link
  it to the payroll record only when payroll locks.
- **FR-007**: The system MUST retain loan history and derive the outstanding
  balance from principal and deducted installments.
- **FR-008**: The system MUST record debt charges, adjustments, and reversals as
  positive-amount transactions, retaining every original entry.
- **FR-009**: The system MUST prevent duplicate reversal of a debt transaction
  and prohibit ordinary reversal of a settled transaction.
- **FR-010**: The system MUST apply employee, branch, department, and finance
  role scope on all finance actions and reads.
- **FR-011**: The system MUST provide payroll only approved advances, due
  scheduled loan installments, and unsettled debt entries for its period.

### Key Entities *(include if feature involves data)*

- **Advance request**: A monthly requested amount, status, requester, and decision.
- **Loan**: An approved principal and count with a repayment schedule.
- **Loan installment**: A dated due amount and optional payroll settlement link.
- **Debt type**: The category used to classify a ledger entry.
- **Debt transaction**: An immutable charge, adjustment, or reversal linked to an
  employee and optionally to an original entry and payroll settlement.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All tested advance boundaries at day 19/20, worked days 19/20,
  half salary, and zero/negative projected net pay produce the expected result.
- **SC-002**: For 100 tested loan principals, installment amounts sum exactly to
  the principal with no cent lost or created.
- **SC-003**: A payroll retry never deducts a loan installment twice in tested
  scenarios.
- **SC-004**: After 100 tested debt reversals, every original and reversal is
  still visible and balances reconcile.
- **SC-005**: All tested out-of-scope finance actions are denied before any write.

## Assumptions

- Person A supplies employee scope and effective salary context; Person C
  supplies projected net pay, payroll locks, and the settlement transaction.
- Worked days are counted from accepted attendance for the request month through
  the request date; only `present` and `late` count.
- Monetary values are expressed to two decimal places, and installment remainders
  are assigned to the earliest installment.
- Direct changes to a locked payroll period use Person C's tracked adjustment
  workflow. Schema and migrations remain frozen.
