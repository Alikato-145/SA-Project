# C4 Validation Quickstart

## Prerequisites

- Use the C4 branch in both `backend/` and `frontend/`.
- Configure the existing PostgreSQL environment and session/authentication
  settings.
- Seed or create representative Employee, Supervisor, Branch Manager, HR, and
  Owner accounts with scoped roles and assigned employees.
- Run `cd backend && bun run db:seed` to create the idempotent demo fixture:
  its employee assignment, Sunday holiday, branch schedule, required payroll
  configurations, current payroll period, and current-month attendance are
  included for C4 smoke testing.

## Package validation

```sh
cd backend
bun run typecheck
bun test

cd ../frontend
bun test
bun run lint
bun run build
```

## Live role smoke

1. Sign in as HR and create/list an employee-linked daily-workflow record.
2. Sign in as a supervisor and confirm the allowed department record is visible
   while an out-of-department record is safely denied.
3. Sign in as an employee and submit/list only that employee's leave, overtime,
   or finance request.
4. Confirm a supervisor cannot approve a four-day leave, then confirm a branch
   manager can approve it in scope.
5. Confirm a pending overtime is not payable until approved.
6. Confirm an approved finance input is visible to payroll preview but is not
   settled until payroll lock.
7. Verify dashboard shell account identity, permitted navigation, and sign-out.
8. Check each released workflow at 360px and 1280px: visible task heading,
   obvious primary action, readable status, and no horizontal page scrolling.

## Expected result

Every endpoint uses an authenticated session and a stable envelope; the role
matrix denies out-of-scope access server-side. Existing payroll, approval, and
financial-history constraints remain unchanged.

## Recorded package validation — 2026-09-28

- Backend: `bun run typecheck` passed; `bun test` passed with database-only checks skipped when `TEST_DATABASE_URL` is absent.
- Frontend: `bun test`, `bun run lint`, and `bun run build` passed.
- Impeccable detector: no actionable finding for the changed dashboard shell and Operations pages.
- Live PostgreSQL role smoke: PostgreSQL migration and development role seed ran in an isolated container on port `5433` (port `5432` belonged to another project). HR session access to `GET /api/v1/operations/advance-requests?employee_id=1` returned `200` with the standard envelope. An Employee request for another employee's leave records returned safe `404 RESOURCE_NOT_FOUND` without disclosing a record. The full workflow matrix remains pending because the supplied seed has no effective employment assignment, schedules, attendance, or payroll configuration needed to create/approve operational facts.
