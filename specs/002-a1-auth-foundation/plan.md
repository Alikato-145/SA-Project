# Implementation Plan: A1 Authentication Foundation

**Branch**: `002-a1-auth-foundation` | **Date**: 2026-09-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-a1-auth-foundation/spec.md`

## Summary

Deliver the backend authentication and authorization foundation for Haris Payroll:
password login, an eight-hour signed JWT in an HTTP-only cookie, logout,
current-actor lookup, atomic five-attempt/15-minute lockout, account and fixed-role
administration, fresh database-backed role scopes on every protected request, stable
public errors, request correlation, and audit observation for every backend action.
Mutations write redacted audit facts in the same transaction; reads and failures write
outcome facts separately. The implementation reuses the frozen PostgreSQL model and
does not change migrations or shared application composition.

## Technical Context

**Language/Version**: TypeScript 5.9 on Bun 1.3.11

**Primary Dependencies**: Elysia 1.4.x, Drizzle ORM 0.44.x, node-postgres,
`@elysiajs/jwt` compatible with Elysia 1.4, Zod 4; Elysia core cookie support and
`Bun.password` Argon2id

**Storage**: PostgreSQL 16 using existing `user_accounts`, `roles`,
`user_account_roles`, `employees`, organization scope tables, and `audit_logs`

**Testing**: Bun test runner, TypeScript `tsc --noEmit`, isolated PostgreSQL
integration fixtures, Elysia route integration tests

**Target Platform**: Bun backend on Linux/Alpine containers and supported local Bun
development environments; browser client over the existing gateway

**Project Type**: Feature-first web-service backend in a repository with separate
backend and frontend Git submodules

**Performance Goals**: Normal authenticated requests perform one current-actor/grant
lookup and complete within 500 ms in the demo environment; sign-in may take longer
because password verification is intentionally expensive but completes within 2 s

**Constraints**: Frozen schema/migrations; eight-hour stateless token; no refresh or
server revocation; current roles apply on the next request; every use case is
observed; no secrets or full sensitive identifiers in responses/errors/logs/audit;
Person A exports route plugins but does not edit `backend/src/app.ts`

**Scale/Scope**: Five fixed roles, one optional employee link per account, low-volume
restaurant workforce, approximately 20 A1 actions/endpoints, one backend package and
no A1 frontend screens (login/account UI belongs to A4)

## Constitution Check

*GATE: Passed before Phase 0 and re-checked after Phase 1.*

### Pre-Design Gate

| Principle | Result | Evidence |
|---|---|---|
| Historical Payroll Integrity | PASS | A1 does not update payroll/history tables; account and role mutations are audited and never require hard deletion. |
| Server-Enforced Authorization and Atomic Decisions | PASS | Current DB grants are evaluated in services for every protected action; account/role mutations and domain audit are transactional. |
| Feature-First Layered Backend | PASS | Route → controller → service → repository → database is preserved; only repositories query Drizzle. |
| Data Model and Contract Discipline | PASS | Existing PostgreSQL/Drizzle model is reused; mismatches are documented without migration edits; public errors are stable and redacted. |
| Focused Verification and Minimal Change | PASS | Tests focus on lockout, JWT/cookie, origin, scopes, escalation, audit atomicity, and secret redaction. |
| Domain-Specific Constraints | PASS | A1 establishes actor/scope/audit foundations without changing attendance/payroll business facts. |
| Workflow and submodule discipline | PASS | Implementation is confined to `backend/`; `app.ts` composition and root submodule pointer remain coordinator-owned. |

No constitution violations require justification.

### Post-Design Gate

| Principle | Result | Design confirmation |
|---|---|---|
| Historical integrity | PASS | Audit repository exposes insert/read only; the database append-only trigger remains authoritative. |
| Authorization and atomicity | PASS | Authenticated actor reloads status/grants each request; mutation audit shares the business transaction. |
| Layering | PASS | Contracts name route/controller/service/repository/mapper responsibilities and cross-feature service boundaries. |
| Data/contract discipline | PASS | `record_id` sentinels and action suffixes fit existing columns; no schema extension is hidden in JSON. |
| Verification/minimal change | PASS | One new runtime dependency; role bootstrap and tests are explicitly scoped; no frontend or unrelated business work. |

## Technical Decisions

1. **Session token**: HS256 JWT with only `sub`, `iat`, and `exp`; roles/status are not
   embedded. Cookie `haris_session` is HTTP-only, `SameSite=Lax`, path `/`, max age
   28,800 seconds, and secure in production.
2. **Password**: `Bun.password` Argon2id. Unknown usernames verify against a fixed
   dummy hash to reduce user-enumeration timing differences.
3. **Lockout**: Login locks the account row before checking/updating attempts. Invalid
   attempts commit their counter/lock change and audit fact before returning the error.
4. **Current actor**: Each protected request verifies the token, then reloads account,
   optional employee, active roles, and grants from PostgreSQL.
5. **CSRF/origin**: Login, logout, and all cookie-authenticated mutations require an
   exact allowed `Origin`; JSON mutations require the JSON content type.
6. **Audit action convention**: `<domain>.<resource>.<verb>.<outcome>` where outcome is
   `succeeded` or `failed`, maximum 80 characters. Targets without a concrete ID use
   `record_id` sentinels `unknown`, `self`, or `collection`.
7. **Audit transaction rule**: Successful mutation facts share the business
   transaction and fail closed. Failed actions append after rollback. Read actions
   append before the response returns.
8. **Audit redaction**: Event-specific allowlists are primary; a recursive denylist is
   defense-in-depth. Raw bodies, headers, thrown errors, and credentials never reach
   the audit repository.
9. **Fixed roles**: An idempotent bootstrap creates or validates five role masters;
   there is no role CRUD.
10. **Temporary passwords**: Generated and shown once. The frozen schema has no
    forced-first-change field, so first-login rotation is deferred.
11. **Role administration**: Owner may administer every fixed role. HR may administer
    all roles except `OWNER`; disabling or removing the final active Owner is rejected.
12. **Audit cardinality**: One canonical audit row per endpoint invocation. For a
    mutation success, the transactional domain row is that canonical row; observers
    do not insert a duplicate transport-success row.

## Project Structure

### Documentation (this feature)

```text
specs/002-a1-auth-foundation/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── auth-api.md
│   └── audit-observer.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/src/
├── app.ts                              # Person C composes plugins; A1 does not edit
├── core/
│   ├── config/{env.config.ts,auth.config.ts}
│   ├── db/transaction.ts               # shared dependency coordinated with Person C
│   ├── errors/{application.error.ts,error-codes.ts,error-boundary.ts}
│   ├── auth/{auth.types.ts,password.ts,session-token.ts,csrf-origin.ts,
│   │         authenticated-actor.ts,authorization.ts,auth.plugin.ts}
│   └── audit/{action-context.ts,audit-redaction.ts,action-observer.ts,
│             domain-audit-observer.ts,request-id.plugin.ts}
├── shared/http/http.dto.ts              # contract coordinated with Person C
└── features/
    ├── audit/{audit.repository.ts,audit.service.ts,audit.dto.ts,audit.mapper.ts,
    │           audit.controller.ts,audit.routes.ts,*.test.ts}
    ├── user-account/{user-account.repository.ts,user-account.service.ts,
    │                  user-account.dto.ts,user-account.mapper.ts,
    │                  user-account.controller.ts,user-account.routes.ts,
    │                  user-account.validation.ts,*.test.ts}
    └── role/{role.repository.ts,role.service.ts,role.dto.ts,role.mapper.ts,
              role.controller.ts,role.routes.ts,role.bootstrap.ts,*.test.ts}
```

**Structure Decision**: Use the mandated feature-first backend layout. Technical
cross-cutting policies stay in `core/`; public account/role/audit behavior stays in
its owning feature. Each feature exports a plugin for later composition.

## Dependency and Delivery Order

```text
error/request-id contracts
  → transaction executor contract
  → audit repository/redaction/observers
  → password/JWT/origin primitives
  → account repository + login lockout
  → authenticated actor + authorization evaluator
  → role bootstrap and account/role administration
  → controllers/routes/error boundary
  → route, authorization-matrix, and audit-atomicity validation
```

The shared `transaction.ts`, response envelope, and `app.ts` registration are
coordinated boundaries. A1 must not duplicate transaction policy inside a feature.

## Known Schema/Model Mismatches

- The approved service rule requires department grants to contain both `branch_id`
  and `department_id`; the current trigger permits department without branch. A1
  enforces the stricter service rule and records a schema-owner follow-up.
- The model has no `must_change_password` or `password_changed_at`; temporary
  passwords are one-time display values but ordinary credentials thereafter.
- Persistent audit cannot be guaranteed while PostgreSQL itself is unavailable
  because audit and business data share the same store. A redacted operational-log
  fallback records the outage without claiming database durability.

## Complexity Tracking

No constitution violations require an exception. The two-level observer is necessary
to satisfy atomic mutation evidence and failure/read outcomes: a route-only hook
misses domain facts, while a service-only wrapper misses pre-service validation.
