# A1 Authentication Foundation Handoff

## Verification result

Validated on 2026-09-22 against the isolated PostgreSQL database
`haris_payroll_a1_verify_0922`, created only for A1 verification and migrated with
the repository's frozen Drizzle migration.

```text
bun run db:migrate
  migrations applied successfully

bun test
  116 pass
  0 fail
  396 assertions
  25 files

bun run typecheck
  passed (tsc --noEmit)
```

## Runnable scenario evidence

| Quickstart scenario | Evidence |
|---|---|
| Lockout boundary | `user-account.service.test.ts` covers attempts 1-4, fifth-attempt lock, correct password during lock, exact expiry, disabled account, unknown-user dummy verification, concurrent serialization, and one audit outcome. |
| Current grants and revocation | `auth.plugin.test.ts` proves account disablement and role revocation apply on the next request using an unexpired token. |
| Account administration | `user-account.admin.test.ts`, `account.routes.test.ts`, `role.service.test.ts`, and `role.routes.test.ts` cover create/link, one-time password, status/reset/unlock, fixed scopes, HR-to-Owner denial, privilege containment, and final-Owner protection. |
| Audit atomicity | `audit.integration.test.ts` passes against PostgreSQL for mutation rollback, separately committed failure audit, and database append-only triggers. |
| Secret scan | `audit.secret-scan.test.ts` scans audit payloads, public errors, fallback logs, and response DTOs; temporary password is permitted only in create/reset responses. |
| Registered actions | `audit.completeness.test.ts` inventories all 13 A1 endpoints, validates one canonical pre-service failure, and excludes health, preflight, static, unknown routes, and audit insertion. |

## Composition handoff

The shared application composer should register, without moving business logic:

1. request-ID and `createA1TransportAuditPlugin` once at the A1 boundary;
2. `createAuthPlugin` with the repository-backed authenticated actor loader;
3. authentication routes, account-administration routes, fixed-role routes, and
   audit-history routes;
4. the shared public error boundary.

`backend/src/app.ts` was intentionally not edited because it is owned by the shared
composition work.

## Known limitations

- Stateless logout clears the cookie but cannot revoke a copied token before its
  eight-hour expiry. Disablement and role revocation still apply on the next request.
- Password reset does not revoke existing tokens. Disable the account when immediate
  invalidation is required.
- The frozen schema cannot enforce a mandatory first-password change.
- Department/branch consistency is stricter in the service than the current database
  trigger; the schema-owner follow-up remains documented in `research.md`.
