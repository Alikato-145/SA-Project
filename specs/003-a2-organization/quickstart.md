# A2 Organization Quickstart

## Preconditions

1. Configure the same test environment used by A1, including a valid
   `AUTH_JWT_SECRET`, `AUTH_ALLOWED_ORIGINS`, and isolated PostgreSQL database.
2. Apply the existing migrations. A2 adds no schema or migration.
3. Mount the four exported organization route modules in a test-only Elysia
   composition. Do not edit the shared `src/app.ts` during A2.
4. Seed active Owner, HR, branch-manager, supervisor, and employee accounts with
   representative active and revoked grants.

## Scenario 1 — Build a hierarchy

As Owner or HR:

1. Create a shop.
2. Create a branch under that shop, omitting timezone to verify
   `Asia/Bangkok` is applied.
3. Create a department under the branch.
4. Create a position under the shop.
5. Read each detail and list the hierarchy.

Expected: all identifiers are decimal strings, parent IDs remain stable, and
each endpoint invocation has exactly one correlated audit outcome.

## Scenario 2 — Verify scoped reads

1. Give a branch manager a grant for one branch.
2. Give a supervisor a grant for one department in that branch.
3. Create another branch and department under the same shop and another shop.
4. List/detail all four resources as each actor.

Expected: Owner/HR see all permitted records; the branch manager sees only the
granted branch, its departments, parent shop, and shop positions; the
supervisor sees only the granted department, required parents, and shop
positions. Employee self scope fails closed without A3 assignment context.

## Scenario 3 — Exercise boundaries

1. Reuse a branch code under a different shop: accepted.
2. Reuse it under the same shop: `DUPLICATE_CODE`.
3. Repeat for department-by-branch and position-by-shop uniqueness.
4. Submit invalid and overlong text and unsafe decimal identifiers:
   `VALIDATION_ERROR`.
5. Submit a non-IANA timezone: `VALIDATION_ERROR`.

Expected: rejected requests make no business mutation and expose no database
details.

## Scenario 4 — Preserve history

1. Deactivate a shop, branch, department, and position using a non-empty reason.
2. Repeat each deactivation.
3. Explicitly request inactive records.
4. Attempt to create a new child under an inactive parent.
5. Inspect the route table for `DELETE` methods.

Expected: the first deactivation succeeds without cascading; repeats and
inactive-parent creation return `STATE_CONFLICT`; historical details remain
readable; no hard-delete route exists.

## Scenario 5 — Full verification

Run from `backend/`:

```sh
bun run typecheck
bun test
```

Then run the isolated PostgreSQL integration suites and verify:

- no regression in A1 tests;
- authorization scope, pagination, filtering, uniqueness, parent activity,
  timezone, immutable parents, and deactivation tests pass;
- mutation and audit rows commit or roll back together;
- all 20 endpoint contracts are registered and none uses `DELETE`.
