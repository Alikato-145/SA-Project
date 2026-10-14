# Human UAT — Haris Payroll

Use a separate acceptance database with synthetic data. Automated tests are in
release-verification-2026-10-14.md; this sheet is intentionally unsigned until
real representatives execute their duties. Record the exact root revision first.

| Role | Acceptance journey | Result / tester / date |
|---|---|---|
| Owner | Initial access; organization/account/scope setup; schedules/config; payroll readiness; locked totals and management reports | Pending |
| HR/accounting | Onboarding; assignment/holiday/bank histories; attendance correction; quota setup; leave/OT/finance; preview/lock; adjustment; PDF/CSV/email history | Pending |
| Branch manager | Own-branch staff/attendance; approve a four-day leave directly; OT decision; read scoped payroll; deny another branch | Pending |
| Supervisor | Own-department staff; approve up to three days with corrected type; deny four-day and another department; inspect decision history | Pending |
| Employee | Own profile/leave/OT/advance; own payslip PDF; no admin actions; direct cross-employee request denied; password/logout | Pending |

Check Thai labels, keyboard navigation, 360px phone layout, error recovery and
month entry on the devices the organization will actually use. Compare export
encoding/columns with the accounting recipient's required bank/SS format.

Before real hosting: resolve or accept tracked vendor image findings, configure
TLS/secrets/alerts, approve encrypted off-host backup retention and RPO/RTO, and
replace SMTP mock values. Send a synthetic payslip only to an explicitly authorized
recipient. CSV generation does not confirm a bank payment or SS submission.

Record failures with role, page, inputs (no secrets), expected/actual outcome and
request ID. No audit, debt history or locked payroll should be manually edited to
make an acceptance case pass.
