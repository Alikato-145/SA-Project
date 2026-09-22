# B3 API and Integration Contract

Person C mounts exported B3 routes under `/api` and supplies actor context,
public error mapping, and payroll settlement.

| Route | Purpose |
|---|---|
| `POST /advance-requests` | Submit a monthly request. |
| `GET /advance-requests?employee_id=:id` | Read scoped requests. |
| `POST /advance-requests/:id/approve` | Recheck eligibility and approve. |
| `POST /advance-requests/:id/reject` | Reject a pending request. |
| `POST /loans` | Create an approved loan and installments. |
| `GET /loans?employee_id=:id` | Read loan and schedule. |
| `POST /debt-transactions` | Record a charge or adjustment. |
| `POST /debt-transactions/:id/reverse` | Append a reversal. |
| `GET /debt-transactions?employee_id=:id` | Read the ledger and balance. |

Person A: actor scope and effective salary context. Person B1: accepted work-day
count. Person C: projected net pay and payroll lock transaction. Payroll readers
provide approved advances for a month, scheduled due installments, and unsettled
debt entries. Public error codes include `OUT_OF_SCOPE`,
`ADVANCE_INELIGIBLE_DATE`, `ADVANCE_WORK_DAYS_INSUFFICIENT`,
`ADVANCE_HALF_SALARY_EXCEEDED`, `ADVANCE_NEGATIVE_NET_PAY`,
`ADVANCE_ALREADY_EXISTS`, `LOAN_INVALID_INSTALLMENTS`,
`LOAN_ALREADY_DEDUCTED`, `DEBT_ALREADY_REVERSED`, and
`DEBT_ALREADY_SETTLED`.

Request bodies use snake_case as in the route schemas. Successful response
DTOs use the existing Person B camelCase response convention; money remains
decimal strings and IDs remain numeric in this sprint contract.

**Debt settlement blocker**: `debt_transactions_append_only` rejects updates,
including the settlement fields. Person C and the schema owner must agree on a
recorded settlement mechanism before payroll can consume debt safely. B3's
ledger creation and reversal remain available; the payroll reader is a
read-only candidate list until that decision.
