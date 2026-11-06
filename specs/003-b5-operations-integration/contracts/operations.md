# Operations Contract

All routes are under `/api/v1`. Trusted session cookie is required. Cookie mutations validate origin using shared policy. Success is `{ data, request_id }`; failures are `{ error: { code, message }, request_id }` with stable public codes. Public fields use snake_case; IDs are positive decimal strings; money/quantities remain decimal strings; dates are ISO business dates and timestamps timezone-aware ISO strings. Unknown fields, invalid dates/enums/amounts, unsafe IDs and forged actor fields are rejected.

| Feature | Reads | Mutations |
|---|---|---|
| Schedule | GET /branch-schedules?branch_id; GET /branch-schedules/applicable?branch_id&work_date | POST /branch-schedules; PATCH /branch-schedules/:id creates successor; PUT /branch-schedules/:branch_id/overrides/:date |
| Holiday | GET /holiday-calendars?shop_id&holiday_date&active_only | POST /holiday-calendars; PATCH /holiday-calendars/:id |
| Attendance | GET /work-day-records?employee_id or branch_id&start_date&end_date | POST /work-day-records; PATCH /work-day-records/:id |
| Leave | GET /leave-requests?employee_id; GET /leave-types; GET /leave-quotas?employee_id&quota_year; GET /leave-requests/:id/history | POST /leave-requests; POST /leave-requests/:id/approve or /reject |
| OT | GET /overtime-records?employee_id; GET /overtime-records/:id/history | POST /overtime-records; POST /overtime-records/:id/approve or /reject |
| Advance | GET /advance-requests?employee_id | POST /advance-requests; POST /advance-requests/:id/approve or /reject |
| Loan | GET /loans?employee_id includes installments | POST /loans |
| Debt | GET /debt-transactions?employee_id returns entries/balance/outstanding_balance | POST /debt-transactions; POST /debt-transactions/:id/reverse |

Attendance payload: employee_id, branch_id, work_date, status, optional clock_in_at/clock_out_at, late_minutes, is_deductible, note. Service validates/derives schedule context. Leave: employee_id, leave_type_id, start_date, end_date, reason, is_retroactive; approve accepts optional final_leave_type_id. OT: employee_id, overtime_date, overtime_type, hours or day_units, optional work_day_record_id/reason. Finance fields follow existing snake_case request shapes with string identifiers. No public settlement mutation: payroll locks settle eligible inputs transactionally.

Authorization: Employee owns self requests/reads; supervisors manage department attendance and leave/OT decisions subject to approval limit; branch managers manage their branch; HR/owner manage authorized global workflows. Finance approval/loan/debt administration belongs to global HR/owner duties unless an existing confirmed policy grants it otherwise. Grant association is preserved. History/quota reads enforce the same target scope.

Payroll service dependencies expose transaction-aware input mutability and advance projection; callers never query another feature repository. Lock rejects source mutations for protected dates and snapshots a consistent set. Pending approvals are evaluated only for the relevant shop/period.

Debt settlement response fields are derived from immutable locked payroll source items; original debt transaction rows remain append-only. Repeated deductions and post-settlement reversals are rejected. See [schema-owner handoff](../schema-owner-handoff.md).

Ledger balance is the historical net charge total. outstanding_balance is the exact decimal total of unconsumed, non-reversed obligations. Settled entries retain derived settled_at and settled_in_payroll_record_id evidence without rewriting their raw row. Approved leave creates no payroll deduction regardless of legacy leave-type classification.
