# Quickstart Validation: A1 Authentication Foundation

This guide is used after implementation. It does not authorize schema or migration
changes.

## Prerequisites

- PostgreSQL infrastructure feature is complete and the frozen migration is applied.
- A test environment provides a strong JWT secret and exact allowed frontend origins.
- Five fixed roles and one initial Owner are provisioned through the controlled setup.
- Person C's transaction and HTTP response contracts are available.

## Environment

Use non-production test values; never commit secrets:

```text
AUTH_JWT_SECRET=<at least 32 random bytes>
AUTH_ALLOWED_ORIGINS=http://127.0.0.1,http://localhost
NODE_ENV=test
AUTH_SESSION_TTL_SECONDS=28800
AUTH_MAX_FAILED_ATTEMPTS=5
AUTH_LOCK_DURATION_SECONDS=900
```

## Focused checks

From `backend/`:

```bash
bun run typecheck
bun test src/core/errors
bun test src/core/auth
bun test src/core/audit
bun test src/features/user-account
bun test src/features/role
bun test src/features/audit
```

Expected: all checks pass; a run with no discovered tests is not acceptable evidence.

## Scenario 1: Lockout boundary

1. Provision an active account.
2. Submit wrong passwords four times; each returns `INVALID_CREDENTIALS` and remains unlocked.
3. Submit the fifth wrong password; it returns the locked outcome and records a 15-minute lock.
4. Submit the correct password during the lock; it remains denied.
5. Advance the controlled clock to expiry and sign in successfully.
6. Confirm failed count/lock clear and `last_login_at` is set.
7. Confirm exactly one redacted audit fact per invocation and no submitted password/username in unknown-user facts.

## Scenario 2: Current grants and revocation

1. Sign in as an account with a department grant.
2. Access same-department data successfully and other-department data unsuccessfully.
3. Revoke the grant as Owner.
4. Reuse the unexpired cookie on the next protected request.
5. Confirm access is denied because current grants are reloaded.

## Scenario 3: Account administration

1. As Owner, create an employee-linked account and receive one temporary password.
2. Confirm that the password cannot be retrieved through account detail or audit.
3. Grant Supervisor with matching branch/department.
4. Reject missing branch, mismatched department, and duplicate grant.
5. Disable the account and confirm its existing cookie fails on the next request.
6. Confirm HR cannot grant Owner and the final active Owner cannot be disabled.

## Scenario 4: Audit atomicity

1. Force a domain audit insert failure during an account mutation.
2. Confirm no account mutation committed.
3. Force a business constraint failure after the transaction begins.
4. Confirm the business change rolled back and one failed audit fact persisted afterward.
5. Attempt audit update/delete and confirm existing database protection rejects it.

## Scenario 5: Secret scan

Exercise every A1 endpoint success and failure fixture, then assert that responses,
captured logs, and serialized audit payloads contain zero occurrences of the fixture's:

- password and temporary password (except the one intended response field),
- hash, JWT, cookie, authorization value,
- full national/passport identifier,
- full bank account or ciphertext.

## Full backend validation

```bash
bun run typecheck
bun test
```

After Person C composes the plugin, validate the complete stack from the repository root:

```bash
docker compose up --build -d
docker compose ps
curl --fail http://127.0.0.1/healthz
```

Record commands and results in the A1 handoff. Do not update the root backend submodule
pointer from the A1 feature work.

## Known session and credential limitations

- Logout clears the browser cookie but a copied stateless token remains valid for
  at most the configured eight-hour lifetime.
- Password reset does not revoke existing stateless tokens. Disable the account
  when immediate invalidation is necessary; protected requests reload status.
- The frozen schema cannot record or enforce a mandatory first-password change.
