# Research: Employee Finance

## Advance decision

**Decision**: Evaluate the request date, worked-day count, half of base salary,
and projected net pay at approval time. Store the month as its first day and
translate the unique employee/month conflict.

**Rationale**: Facts can change between submission and approval; a stale
eligibility preview must not approve an invalid deduction.

**Alternatives considered**: Client-only and submission-only checks were rejected.

## Exact money

**Decision**: Parse two-decimal strings into integer cents. Split a loan principal
using integer division and allocate the remaining cents to the earliest due
installments.

**Rationale**: Every scheduled amount must sum exactly to the principal.

**Alternatives considered**: Floating-point division was rejected.

## Loan settlement

**Decision**: Create the loan and all installments in one transaction. Payroll
reads scheduled due installments; Person C's payroll lock operation changes them
to deducted and links the payroll record atomically.

**Rationale**: A preview must not consume an installment.

## Debt ledger

**Decision**: Store positive amounts for charge, adjustment, and reversal.
Calculate the signed balance from kind; a reversal is a new linked transaction.
Reject a second reversal and an ordinary reversal after settlement.

**Rationale**: The migration makes debt transactions append-only.

**Confirmed integration conflict**: The same trigger rejects all updates and
deletes, so payroll cannot later fill `settled_at` or
`settled_in_payroll_record_id` on an existing debt entry. Person C and the
schema owner must decide an append-only settlement representation or a reviewed
schema exception before automatic settlement is exposed. B3 does not alter the
frozen migration or pretend settlement is complete.

## Integration

**Decision**: Inject Person A's effective salary/scope context and Person C's
projected net-pay and payroll lock contracts. Expose B3 service readers for C.
