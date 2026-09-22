# B1 Validation Guide

## Prerequisites

- Person C has composed B1 routes with authenticated actor context.
- A disposable database has organization, branch, employee, assignment and account
  fixtures supplied by Persons A/C.
- `TEST_DATABASE_URL` points to that migrated database.

## Package checks

```bash
cd backend
bun run typecheck
bun test src/features/branch-schedule/branch-schedule.test.ts
bun test src/features/holiday-calendar/holiday-calendar.test.ts
bun test src/features/attendance/attendance.test.ts
TEST_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:55433/haris_payroll bun test
```

Expected: tests cover authorization before persistence, schedule selection,
override-hour rules, holiday activation, duplicate records, clock validation,
manual source and historical branch snapshot. The opted-in suite verifies frozen
database constraints.

## Manual flow

1. Create a branch schedule effective on a known date.
2. Add a closed or replacement-hours override and confirm it takes precedence.
3. Add an active holiday, confirm it returns, deactivate it, and confirm it is absent.
4. Create an employee work-day record with explicit branch and manual source.
5. Submit a duplicate and an inverted clock range; confirm stable validation errors.
6. Correct the record and retrieve it by payroll date range; its branch must persist.
7. Repeat with an out-of-scope actor and confirm no write occurs.

## Handoff checks

Before routes are enabled, C confirms [integration.md](contracts/integration.md),
especially the payroll-lock guard for attendance corrections.
