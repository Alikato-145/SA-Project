# B3 Data Model

| Entity | Key fields | Invariants |
|---|---|---|
| Advance request | Employee, month, amount, status, requester/decider | Unique employee/month; positive two-decimal amount; month stored as first day. |
| Loan | Employee, principal, reason, installment count, approver | Positive principal; count from 1 to 5. |
| Loan installment | Loan, sequence, due month, amount, status, payroll link | Positive amount; one sequence number per loan; due month starts on day 1. |
| Debt type | Code, name, active state | A charge requires an active type. |
| Debt transaction | Employee, type, kind, date, amount, original/settlement references | Positive amount; append-only; reversal points to original and occurs at most once. |

Advance states: `pending → approved|rejected`. Loan installments:
`scheduled → deducted` only with payroll lock; `waived` is outside B3's
ordinary flow. Debt records never transition by update or delete.
