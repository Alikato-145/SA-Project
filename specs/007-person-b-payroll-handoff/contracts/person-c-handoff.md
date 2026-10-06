# Person C Integration Handoff

- Mount B1–B3 route factories under `/api` with A's authenticated actor/scope and C's stable error boundary. B4's four routes call these same-origin paths.
- Inject A's effective assignment branch lookup into B1's leave attendance effect. Pass that effect to `LeaveService` and C's payroll-period guard to attendance, leave, and OT services. The leave effect must receive LeaveService's transaction unchanged.
- For advance eligibility, adapt B1 `AttendanceService.countWorkedDaysForAdvance(actor, employeeId, monthStart, requestDate)` as B3 `AdvanceEligibility.getWorkedDays`; it counts only present/late records and enforces scoped read. A supplies base salary effective on the request date. C supplies projected net pay after all deductions.
- For payroll calculation, consume B1 `findForPayrollRange`, B2 `findApprovedForPayroll` for leave and OT, B3 `findApprovedForPayroll` for advances, `findDueForPayroll` for loans, and debt candidate entries. Do not infer OT from clock-out or include pending requests.
- Locking must call B3's `markDeducted` for loan installments in C's payroll transaction. The lock adapter receives payroll record ID, installment employee ID, and due month; it must verify the locked payroll record belongs to that employee and covers the due installment.
- **Blocking decision**: the frozen `debt_transactions_append_only` trigger rejects updates to `settled_at` and `settled_in_payroll_record_id`. C and schema owner must choose a settlement link (for example, locked `payroll_items` source references with uniqueness/idempotency) before debt may be deducted in payroll. B's debt reader remains a candidate reader and must not be interpreted as proof of settlement.
- The app shell/nav, frontend `/api` routing, auth adapters, error DTO, payroll service, and DB fixtures are C/A-owned and absent here. No B-owned file can complete the live demo without those integrations.

B1 now rejects manual `leave` status and ordinary corrections to leave rows.
Only the injected leave-approval effect writes that status. C should coordinate
its payroll lock guard with attendance corrections, because a guard check and
later update must not race with a period lock.
