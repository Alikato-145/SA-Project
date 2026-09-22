# B2 Validation Guide

From `backend/`, run:

```sh
bun run typecheck
bun test src/features/leave/leave.test.ts src/features/overtime/overtime.test.ts
bun test
```

PostgreSQL checks are opt-in with `TEST_DATABASE_URL` pointing to a disposable,
migrated database. Set `B2_TEST_EMPLOYEE_ID`, `B2_TEST_ACCOUNT_ID`, and
`B2_TEST_LEAVE_TYPE_ID` to existing fixture IDs. The checks roll back their
writes.

Verify three-day versus four-day supervisor approval, quota and attendance atomicity,
type-change history, each OT type/value pair, explicit approval before payroll
visibility, duplicate denial, and immutable decision history.
