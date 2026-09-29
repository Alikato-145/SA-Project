# Research: A1 Authentication Foundation

## Decision 1: Password hashing

**Decision**: Use Bun's asynchronous Argon2id password hashing and verification.

**Rationale**: Bun 1.3.11 already exposes a maintained password API and avoids
another native dependency.

**Alternatives considered**: bcrypt library; custom hashing (unsafe).

## Decision 2: Browser session format

**Decision**: Use `@elysiajs/jwt` for an HS256 JWT containing only account ID and
issued/expiry times, stored in an HTTP-only cookie for eight hours.

**Rationale**: It fits the frozen schema and avoids stale authorization in tokens.

**Alternatives considered**: Database sessions require a migration; token-contained
roles become stale; custom JWT code adds cryptographic risk.

## Decision 3: Account lockout concurrency

**Decision**: Lock the account row in one transaction before password verification
and attempt update. Commit invalid-attempt state plus its audit fact before returning
the public error.

**Rationale**: Concurrent invalid attempts cannot overwrite each other or bypass the
fifth-attempt boundary.

**Alternatives considered**: Unlocked read/update loses increments; in-memory
counters fail across processes and restarts.

## Decision 4: Unknown-user timing path

**Decision**: Verify unknown usernames against a process-initialized dummy Argon2id
hash and always return `INVALID_CREDENTIALS`.

**Rationale**: Reduces observable timing and wording differences.

**Alternatives considered**: Immediate rejection; auditing submitted usernames.

## Decision 5: CSRF/origin policy

**Decision**: Require an exact allowlisted `Origin` on login, logout, and every
cookie-authenticated mutation; reject wildcard origins and require JSON content type.

**Rationale**: `SameSite=Lax` is defense-in-depth, not a complete CSRF boundary.

**Alternatives considered**: SameSite only; stateful CSRF tokens.

## Decision 6: Fresh authenticated actor

**Decision**: Verify token identity, then query account status, optional employee,
and active grants on every protected request.

**Rationale**: Disablement and revocation take effect by the next request.

**Alternatives considered**: Token-contained or cached grants.

## Decision 7: Audit architecture

**Decision**: Use an action observer for every public use case and a domain audit
observer for successful mutations. Mutation audit shares the transaction; failed
actions append after rollback; reads append before response completion.

**Rationale**: One layer cannot cover pre-controller failures and transactional
before/after mutation facts at the same time.

**Alternatives considered**: Database triggers only; route hooks only; service
wrappers only.

## Decision 8: Audit event compatibility

**Decision**: Encode outcome in the action string, error code in `reason`, and use
target sentinels for actions without a concrete record ID.

**Rationale**: Existing columns are sufficient without violating schema freeze.

**Alternatives considered**: New audit columns; raw transport data in JSON.

## Decision 9: Redaction

**Decision**: Construct payloads with event-specific allowlists, then apply a
recursive forbidden-key defense before persistence.

**Rationale**: Denylists alone are easy to bypass with renamed or nested fields.

**Alternatives considered**: Serialize whole requests then delete known keys.

## Decision 10: Role masters and initial administration

**Decision**: Provide an idempotent bootstrap for five fixed roles. Deployment must
provision the initial Owner account through a controlled setup path before ordinary
account administration is used.

**Rationale**: No current seed exists and ordinary Owner/HR-only administration has
a bootstrap cycle.

**Alternatives considered**: Role CRUD; undocumented manual SQL.

## Decision 11: Scope validation

**Decision**: Department scope requires matching branch and department; branch scope
requires branch only; self/all accept neither.

**Rationale**: This is the approved stricter application rule and matches wireframes.

**Alternatives considered**: Rely on the weaker current trigger; edit frozen migration.

## Decision 12: Owner administration safety

**Decision**: Owner may grant/revoke all roles. HR may manage every non-Owner role.
The final active Owner account/grant cannot be disabled or removed.

**Rationale**: Prevents HR from escalating to ownership and avoids administrative
lockout while preserving the confirmed all-branch Owner authority.

**Alternatives considered**: Treat HR and Owner as identical; allow final-owner removal.

## Decision 13: Shared boundaries

**Decision**: A1 exports feature plugins and consumes shared transaction/HTTP
contracts. It does not edit `app.ts` or create duplicate shared abstractions.

**Rationale**: Preserves team ownership and prevents merge conflicts.

**Alternatives considered**: Compose routes directly in `app.ts`; feature-local
transaction helpers.

## Confirmed schema-owner follow-ups

### Department-scope database trigger mismatch

The frozen database trigger permits a department-scoped role without proving the
department belongs to the submitted branch. A1 intentionally applies the stricter
rule in the service: both IDs are required and their organization relationship is
validated. The schema owner should decide whether a later migration should align
the database constraint; A1 does not edit the frozen migration.

### Forced first-password change is not representable

The frozen `user_accounts` table has no field for a temporary-password state,
password-change deadline, or credential version. A1 can return a generated
temporary password exactly once and never persist or audit the plaintext, but it
cannot enforce a first-login password change without a schema decision. This is a
known limitation for the schema owner, not an implicit field or migration in A1.
