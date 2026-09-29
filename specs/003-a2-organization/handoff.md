# A2 Organization Handoff

## Delivery status

A2 is implemented as a composable backend feature. It exposes exactly 20
Shop, Branch, Department, and Position endpoints through
`createOrganizationRoutes`. The feature does not edit `backend/src/app.ts`,
the frozen database schema, or migrations.

The delivered behavior includes:

- Owner and HR all-branch create, update, and one-way deactivation.
- Branch-manager and supervisor scope-intersected reads; employee self scope
  fails closed until A3 provides assignment context.
- Immutable parent identifiers, active-parent checks, deterministic paging,
  inactive-only filtering, IANA timezone validation, and stable public errors.
- Canonical decimal-string IDs are accepted through `Number.MAX_SAFE_INTEGER`;
  unsafe, signed, fractional, exponent, empty, and leading-zero values fail.
- Conditional active-to-inactive updates with no cascade or hard-delete route.
- One transport/domain audit outcome per request, with successful mutations and
  their allowlisted old/new snapshots committed atomically.
- Free-text deactivation reasons stored as trimmed text up to 500 characters;
  stable failure codes remain valid audit reasons.

## Person C composition

The composition root should construct one shared audit service and all four
resource services, then mount the A2 bundle once:

```ts
const audit = createAuditService(db, auditRepository);

const organizationRoutes = createOrganizationRoutes({
  actions: audit.actions,
  services: {
    shops: createShopService({
      repository: shopRepository,
      rootExecutor: db,
      transactionRunner: db,
      audit,
    }),
    branches: createBranchService({
      repository: branchRepository,
      rootExecutor: db,
      transactionRunner: db,
      audit,
    }),
    departments: createDepartmentService({
      repository: departmentRepository,
      rootExecutor: db,
      transactionRunner: db,
      audit,
    }),
    positions: createPositionService({
      repository: positionRepository,
      rootExecutor: db,
      transactionRunner: db,
      audit,
    }),
  },
  authenticate,
  allowedOrigins,
});

app.use(organizationRoutes);
```

`authenticate(request)` is an application-composition adapter. It must read the
`haris_session` cookie, verify the A1 JWT, then reload the current account
status and active grants from persistence. Do not trust roles or scope carried
in request headers or stale token claims. Reuse the same adapter for the A1
audit/account routes where practical.

The bundle already installs the A2 transport-failure observer. Do not install a
second A2 observer around the same routes, or failure requests could be audited
twice. Mount the bundle before calling `.listen()`.

## Quickstart validation

| Scenario | Evidence | Result |
|---|---|---|
| 1. Build a hierarchy | Resource write suites, mutation route suites, and isolated repository runs | Passed |
| 2. Verify scoped reads | Shop/Branch/Department/Position read suites and Department/Position database scope runs | Passed |
| 3. Exercise boundaries | DTO validation, duplicate-code integration, immutable-parent, unsafe-ID, pagination, and timezone cases | Passed |
| 4. Preserve history | Cross-resource deactivation services/routes plus `organization.history.test.ts` | Passed; no cascade and no `DELETE` route |
| 5. Full verification | Typecheck, focused A2, isolated PostgreSQL, full backend regression | Passed |

## Verification record

Run from `backend/`.

### Static and focused A2 checks

```sh
bun run typecheck
bun test <18 focused A2 unit/contract files>
git diff --check
```

Results:

- TypeScript: passed with no diagnostics.
- Focused A2: 118 passed, 7 database-gated skips, 0 failed, 528 assertions.
- Performance fixture: 1,000 records filtered, sorted, and paged in about 4 ms
  against the two-second requirement.
- Whitespace/error check: passed.
- No backend formatter is configured in `package.json`; no dependency was added
  solely to format this delivery.

### Isolated PostgreSQL checks

Use an already migrated isolated database and run each database-bearing file in
its own Bun process because each suite owns and closes its connection pool:

```sh
A2_DATABASE_INTEGRATION=1 DATABASE_URL=<isolated-postgres-url> bun test <a2-db-test-file>
DATABASE_INTEGRATION=1 DATABASE_URL=<isolated-postgres-url> bun test <core-or-audit-db-test-file>
```

A2 isolated file runs completed with 49 passed tests and 0 failures across:

- `shop.write.integration.test.ts`
- `branch.write.test.ts`
- `department.repository.integration.test.ts`
- `department.write.test.ts`
- `position.read.test.ts`
- `position.write.test.ts`
- `organization.history.test.ts`

The pre-existing core database and A1 audit integration files also passed 10
tests with no failures after the audit-reason compatibility change.

### Complete backend regression

```sh
bun test
```

Result: 232 passed, 18 explicitly database-gated skips, 0 failed, 915
assertions across 46 files. Database suites are intentionally opt-in via the
flags above so parallel test files do not close a shared pool out from under one
another.

## Files Person C should mount, not rewrite

- `backend/src/features/organization/organization.routes.ts`
- `backend/src/features/shop/shop.service.ts`
- `backend/src/features/branch/branch.service.ts`
- `backend/src/features/department/department.service.ts`
- `backend/src/features/position/position.service.ts`
- `backend/src/core/audit/a2-transport-audit.plugin.ts`

The public behavior remains defined by
`specs/003-a2-organization/contracts/organization-api.md`.
