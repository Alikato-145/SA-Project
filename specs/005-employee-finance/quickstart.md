# B3 Validation Guide

From `backend/`:

```sh
bun run typecheck
bun test src/features/advance src/features/loan src/features/debt
bun test
```

Use a disposable migrated PostgreSQL database via `TEST_DATABASE_URL` for
constraint checks. Verify day 19/20, worked days 19/20, half salary,
projected net pay, exact installment totals, one-time settlement, reversal
history, and out-of-scope denial.

Validation on 2026-09-22: `bun run typecheck` passed; `bun test` passed 45,
skipped 8 PostgreSQL tests because no disposable `TEST_DATABASE_URL` was set.
B3's exported routes are not mounted in `app.ts` (Person C ownership).
