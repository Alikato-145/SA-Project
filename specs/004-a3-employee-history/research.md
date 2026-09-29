# A3 Research and Design Decisions

## 1. Database baseline and ownership

**Decision**: Use the existing PostgreSQL migration and feature-owned Drizzle schema without A3 migration edits.

**Rationale**: The baseline already enforces unique identity keys, assignment and weekly holiday effective-range exclusions, organization lineage for assignments, and one active primary bank account. The AGENTS guide reserves schema/migration changes to the schema owner.

**Alternative considered**: Rebuild constraints in A3 migrations. Rejected because it changes a frozen shared model and duplicates existing protections.

**Follow-up**: DBML declares `employee_bank_accounts.is_primary` default `false`; Drizzle and the migration use `true`. A3 must explicitly supply `is_primary` for every insert and report the mismatch to the schema owner without changing the migration.

## 2. Date and exact-money semantics

**Decision**: Treat effective date ranges as inclusive business dates. On a change beginning on D, end the former open row on D minus one day and insert a new row beginning D in a single transaction. Monetary APIs use canonical decimal strings with exactly two fractional digits; services must never convert money to JavaScript floating point.

**Rationale**: The PostgreSQL exclusion constraints use inclusive `daterange(..., '[]')`; `numeric(12,2)` is the executable money type. An in-place update of an old salary or welfare row would destroy payroll history.

**Alternative considered**: End the former row on D or update it in place. Both conflict with inclusive dates and the historical integrity rule.

## 3. Organization validation for assignments

**Decision**: The assignment service calls an explicit A2 organization validation service dependency with the same transaction executor to verify active Shop, Branch, Department, Position, and their lineage before insertion. PostgreSQL lineage triggers and FK/overlap constraints remain the final concurrency guard.

**Rationale**: The existing database trigger checks lineage but not active state. A3 must reject inactive masters. Cross-feature repository imports are prohibited by project architecture.

**Alternative considered**: Call public A2 list routes or import the A2 repository directly. Both break the service boundary and cannot reliably validate inside one transaction.

## 4. Optional account creation during onboarding

**Decision**: Add a transaction-aware internal service method to A1 account administration. A3 owns the outer onboarding transaction and invokes the A1 service with that executor. The internal method returns safe account facts to A3, which writes one canonical `employee.profile.onboard` domain audit outcome for the public invocation in the same transaction. The temporary password is returned only after the outer transaction resolves. Direct A1 account endpoints retain their existing independent audit behavior.

**Rationale**: Existing A1 `createAccount` opens its own transaction. Calling it from onboarding would permit a committed account even if later A3 work rolls back.

**Alternative considered**: Import A1 account repository into A3 or call `createAccount` unchanged. Both violate the architecture or atomicity requirement.

## 5. Bank encryption and key version

**Decision confirmed 2026-09-27**: Encrypt plaintext at the service boundary with AES-256-GCM using versioned 32-byte keys loaded from required environment configuration. `EMPLOYEE_BANK_ENCRYPTION_KEY_VERSION` selects the active version and `EMPLOYEE_BANK_ENCRYPTION_KEYS` is a JSON object mapping versions to base64-encoded 32-byte keys. Store an authenticated envelope with a key version, random nonce, ciphertext, and authentication tag in the existing ciphertext field; keep only last four digits separately. The key is never logged, audited, or returned.

**Rationale**: The schema has only ciphertext and last-four columns, and the Person A plan requires an environment secret plus key/version policy. A versioned envelope permits later key rotation without adding a column during A3.

**Alternative considered**: Hardcoded key (unacceptable); unencrypted persistence (violates FR-012); KMS integration (possible if chosen by owner, but expands infrastructure scope).

**Rotation/failure policy**: New writes use the active version; reads/decryption select the version embedded in the authenticated envelope. Deployments retain old keys until re-encryption is complete. Missing, malformed, unknown-version, or authentication failures fail closed without exposing ciphertext or plaintext. Keys are never hardcoded, logged, audited, or returned.

## 6. Audit and transport composition

**Decision**: Reuse A1 `ActionObserver`, `DomainAuditObserver`, redaction allowlists, stable error boundary, and CSRF/origin validation. A3 registers each public action once; successful mutation writes one domain audit outcome in the business transaction, including onboarding; failures write one outcome after rollback. Export a dependency-injected route bundle without editing `app.ts`.

**Rationale**: A1/A2 already establish this observable contract and Person C owns shared application composition.

## 7. Identifiers and scope

**Decision**: Public IDs remain canonical decimal strings that fit the project's current safe-number database driver representation. List/detail repositories intersect current A1 actor grants with current assignment organization. Team views use a separate basic DTO; HR/Owner compensation and own masked-bank views have distinct DTOs.

**Rationale**: This matches A1/A2 contracts and prevents field-level leakage through a single broad response mapper.

## 8. Existing service boundaries verified before implementation

`core/auth/authorization.ts` exports `parseActiveGrant`, which rejects revoked or malformed role/scope combinations. `AuthenticatedActor` carries the linked employee ID and current grants; the request auth plugin is responsible for current account status. `core/db/transaction.ts` exposes `DatabaseExecutor` and `TransactionRunner`. A1 account administration currently opens its own transaction in `createAccount`, so onboarding must use a new transaction-aware *service* port rather than calling that public method. A2 organization scope projection exists, but new assignment validation must use an A2 service method capable of accepting the outer transaction. Existing A1/A2 audit services supply `observeRead`, `observeMutation`, and `domain.record`/`complete`; A3 must avoid double-observing one public action.
