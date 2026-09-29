# Implementation Plan: A3 Employee Master and History

**Branch**: `004-a3-employee-history` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/004-a3-employee-history/spec.md`

## Summary

Deliver scoped employee master reads and writes, effective-dated assignment and compensation history, private bank-account lifecycle, weekly-holiday history, and atomic onboarding on the frozen PostgreSQL model. Reuse A1 actor/audit/error boundaries and A2 organization validation through explicit service dependencies. Export A3 routes for Person C composition; preserve every historical fact.

## Technical Context

**Language/Version**: TypeScript 5.9 on Bun 1.3

**Primary Dependencies**: Elysia, Drizzle ORM, PostgreSQL driver, existing A1 auth/audit/error services, A2 organization service boundary

**Storage**: Existing PostgreSQL 16 tables and migration; no A3 schema edit

**Testing**: `bun:test` unit/contract tests and separate isolated PostgreSQL integration runs

**Target Platform**: Linux web-service container

**Project Type**: Backend feature modules in the existing repository

**Performance Goals**: Correct filtered page of 1,000 employee rows within two seconds in the standard test environment

**Constraints**: Current five-role scope, no hard delete, exact decimal-string money, inclusive effective dates, one canonical audit outcome per public action, encryption before bank persistence, no `app.ts` edit

**Scale/Scope**: Employee master, assignments, bank accounts, weekly holidays, optional account onboarding, date-based downstream context, 16 public A3 endpoints

## Constitution Check

### Pre-design gate

- **Historical Payroll Integrity — PASS**: New effective rows preserve prior organization and compensation; termination/deactivation preserve history.
- **Server-Enforced Authorization and Atomic Decisions — PASS**: Services authorize current actors; onboarding, primary-bank switches, and effective-date changes use one transaction with audit.
- **Feature-First Layered Backend — PASS**: Route → controller → service → repository; response mapping at controller; A1/A2 accessed through explicit service ports.
- **Data Model and Contract Discipline — PASS WITH OWNER FOLLOW-UP**: Existing PostgreSQL migration is canonical. The bank primary default differs between DBML and Drizzle/migration; A3 inserts explicit values and records the mismatch for schema-owner resolution.
- **Focused Verification and Minimal Change — PASS**: A3 adds tests and feature modules; no schema, migration, `app.ts`, attachment, OCR, or payroll implementation changes.

### Bank key gate

Bank implementation and bank-inclusive onboarding wait for owner confirmation of the key/version policy recorded in [research.md](research.md). Independent employee and assignment design remains valid.

## Technical Decisions

1. Repository methods accept a root or transaction executor. Services own transactions, state transitions, authorization, and audit.
2. Employee scope is based on current active A1 grants intersected with current assignment; an Employee self grant uses only its linked `employeeId`.
3. Team/basic, own, and HR/Owner DTOs are distinct, so compensation and private fields cannot leak through a broad mapper.
4. Assignment and holiday ranges are inclusive. A change beginning D closes the prior open row on D minus one day and inserts a new row; PostgreSQL exclusions are concurrency backstops.
5. Assignment org validation goes through an A2 service port inside the A3 transaction. A3 does not import A2 repositories.
6. Money is parsed and handled as canonical `numeric(12,2)` strings. No `Number` conversion for salary or welfare.
7. A1 account administration gains a transaction-aware internal service port for optional onboarding; A3 owns one public onboarding audit outcome.
8. Bank encryption uses a versioned authenticated ciphertext envelope in the existing column, with a required externally supplied key. The exact configuration is pending owner confirmation.
9. Every public A3 action is registered with the transport audit fallback and has one successful or failed outcome. Mutations write their success outcome in the business transaction.
10. `getEmployeeContextAtDate` is a service interface for B/C, returns historical organization and compensation for the requested date, and enforces caller scope.
11. All routes remain independently composable and are exported as one A3 route bundle; Person C owns `app.ts` registration.

## Project Structure

### Documentation (this feature)

```text
specs/004-a3-employee-history/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/employee-api.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source code (repository root)

```text
backend/src/
├── core/
│   ├── audit/                   # A3 action registry and allowlisted snapshots
│   └── errors/                  # A3 stable public errors
└── features/
    ├── employee/                # master, scoped reads, onboarding, route bundle
    ├── employment-assignment/   # effective history and date-based context service
    ├── employee-bank-account/   # encryption, masking, primary lifecycle
    ├── employee-weekly-holiday/ # effective weekday history
    ├── organization/            # A2 transaction-aware validation service port
    └── user-account/            # A1 transaction-aware internal account service port
```

Each feature keeps singular feature-prefixed route/controller/service/repository/mapper/DTO filenames. Existing schema files remain unchanged. Test files live beside their feature code and use `bun:test`.

**Structure Decision**: Preserve feature ownership and the repository's existing layered conventions. The Employee service orchestrates onboarding via explicit cross-feature service dependencies and one unit of work.

## Delivery Order

```text
A1 actor/audit + A2 organization
      ↓
employee scoped reads → employee master writes
      ↓
assignment history + dated context
      ├→ weekly holiday lifecycle
      ├→ bank encryption/primary lifecycle (key gate)
      └→ A1 transaction-aware account port
      ↓
atomic onboarding → nested routes → audit/matrix/integration verification
```

The first runnable slice is scoped employee list/detail. Each later slice has independent focused verification. Bank encryption and full onboarding wait for the key-policy decision; other slices can proceed.

## Post-design Constitution Check

The data model and API contract preserve all pre-design commitments. The bank default discrepancy remains a documented schema-owner follow-up; no migration is changed by Person A. The key policy is an explicit implementation gate, not an implicit hardcoded default.

## Complexity Tracking

No constitution exception is requested.
