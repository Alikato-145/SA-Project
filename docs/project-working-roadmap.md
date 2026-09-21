# Project Working Roadmap

This is the dependency order for getting Haris Payroll from a clone to a usable
application. Complete each gate before starting the next one.

## Gate 1 — Repository can start

1. **PostgreSQL infrastructure alignment**
   - PostgreSQL is the only dialect in Drizzle, migrations, environment files, and Compose.
   - `bun run typecheck`, `bun test`, and clean Compose startup pass.
   - Development and production-like stacks create the same schema.
2. **Runtime smoke check**
   - Gateway, frontend, backend, and PostgreSQL are healthy.
   - `/healthz` and the existing API root respond.

**Done when:** a new contributor runs `docker compose up --build` successfully.

## Gate 2 — Backend foundation

3. **Application error boundary and response contract**
   - Typed application errors map to stable HTTP error DTOs.
4. **Authentication and role scope**
   - User accounts, login/session mechanism, password safety, and server-side role scope.
5. **Database transaction helper**
   - Services can run multi-repository approval/payroll operations atomically.

**Done when:** protected routes can identify an actor and reject out-of-scope access.

## Gate 3 — Organization and employee master data

6. **Organization master data** — shops, branches, departments, positions, roles.
7. **Employee management** — employee records, assignments, salary/welfare history,
   bank accounts, weekly holidays.
8. **Effective-date validation** — prevent overlapping assignments, schedules, and holidays.

**Done when:** HR can create an employee and preserve their employment history.

## Gate 4 — Attendance and approvals

9. **Branch schedules, holidays, and work-day records**.
10. **Leave workflow** — quota, overlap checks, approval history, attendance effects.
11. **Overtime workflow** — request, approval history, payable OT rules.

**Done when:** the system can produce complete, approved attendance for a pay period.

## Gate 5 — Payroll inputs and calculation

12. **Advances, loans, and food-debt transactions**.
13. **Payroll configuration and payroll-period lifecycle**.
14. **Payroll calculation preview** — daily pay, deductions, OT, social security,
    rounding, and non-negative net pay.
15. **Payroll lock and adjustments** — immutable snapshots and tracked corrections.

**Done when:** HR can calculate and lock a valid payroll period without rewriting history.

## Gate 6 — Employee output and operations

16. **Payslips and delivery log** — own-payslip authorization only.
17. **Bank-transfer and social-security exports**.
18. **Audit-log views and operational reports**.

**Done when:** employees receive authorized payslips and accounting can export required reports.

## Per-task checklist

Every numbered item should use `docs/task-spec-guideline.md`, include a focused
test command, and follow the backend flow:

```text
route → controller → service → repository → database
```

For frontend tasks, read `frontend/AGENTS.md` first and keep authorization checks
on the backend.
