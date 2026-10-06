# B2 API Contract for Composition

Person C mounts B2 routes below `/api` with actor context and the shared error
boundary.

| Route | Purpose |
|---|---|
| `POST /leave-requests` | Submit leave. |
| `GET /leave-requests?employee_id=:id` | Read scoped requests. |
| `POST /leave-requests/:id/approve` | Approve with optional final leave type. |
| `POST /leave-requests/:id/reject` | Reject pending leave. |
| `POST /overtime-records` | Submit hourly, rest-day, or public-holiday OT. |
| `GET /overtime-records?employee_id=:id` | Read scoped requests. |
| `POST /overtime-records/:id/approve` | Explicitly approve OT. |
| `POST /overtime-records/:id/reject` | Reject pending OT. |

Public errors: `LEAVE_DATE_OVERLAP`, `LEAVE_QUOTA_EXCEEDED`,
`SUPERVISOR_APPROVAL_LIMIT`, `LEAVE_ALREADY_DECIDED`, `OVERTIME_ALREADY_EXISTS`,
`INVALID_OVERTIME_AMOUNT`, `OVERTIME_CONTEXT_INVALID`, `OVERTIME_NOT_PENDING`,
`OUT_OF_SCOPE`, and `PAYROLL_PERIOD_LOCKED`.

## Required adapters and payroll handoff

Person A supplies effective-date actor scope checks for self submission,
department/branch decisions, and employee reads. B2 services never use a current
assignment to authorize a historical date. Person C supplies the authenticated
actor adapter, the shared error boundary, and payroll-lock guards.

`createLeaveRoutes` and `createOvertimeRoutes` export unmounted Elysia route
modules. C composes them under `/api`. B2's `LeaveService.findApprovedForPayroll`
returns approved dated leave rows with paid/deductible/quota values. Payroll must
read these daily values rather than the request header. B2's
`OvertimeService.findApprovedForPayroll` returns only approved OT records with
type, hours or day units, date, and optional work-day link.

`LeaveAttendanceEffect.applyApprovedLeave(transaction, days)` must be wired to
the attendance feature with the *same* transaction passed by the leave
repository. If this adapter does not use the transaction, leave approval may
partially commit and must not be exposed. The lock guard must check every date
before attendance changes. OT context validation must consult effective weekly
holidays, active shop holidays, and eligible work-day records as appropriate.

The frozen migration excludes overlapping **approved** leave ranges. B2 also
serializes per employee with a transaction-scoped advisory lock and checks
**pending or approved** overlaps before submission, protecting concurrent
requests without a schema change. The executable schema defaults a submitted
request to `pending`; one DBML note refers to `draft`. B2 explicitly writes
`pending` and leaves the frozen model unchanged.
