# Implementation Plan: A2 Organization Management

**Branch**: `003-a2-organization` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/003-a2-organization/spec.md`

## Summary

Implement auditable organization master management for shops, branches,
departments, and positions using the existing frozen PostgreSQL model. Owner and
HR receive all-branch administration; branch managers and supervisors receive
fail-closed scoped reads. Every feature follows route → controller → service →
repository, uses A1 current actors and action/domain observers, prevents parent
reassignment and hard deletion, validates active parents, and exports composable
routes without editing `app.ts`.

## Technical Context

**Language/Version**: TypeScript 5.9 on Bun 1.3

**Primary Dependencies**: Elysia, Drizzle ORM, PostgreSQL driver, A1 auth/audit/error contracts

**Storage**: Existing PostgreSQL 16 organization tables; no schema or migration changes

**Testing**: `bun:test` unit/contract suites plus isolated PostgreSQL integration tests

**Target Platform**: Linux web-service container

**Project Type**: Backend web service in the existing monorepo/submodule structure

**Performance Goals**: Correct filtered pages from 1,000 organization records within two seconds in the standard test environment

**Constraints**: No hard deletes, no parent changes, exact scoped authorization, one canonical audit row per endpoint, decimal-string API IDs, no `app.ts` edit

**Scale/Scope**: Four organization resources, 20 list/detail/create/update/deactivate endpoints, five role types, approximately 1,000 verification records

## Constitution Check

### Pre-Design Gate

- **Historical integrity — PASS**: deactivation replaces deletion; parent identity is immutable; old rows remain readable.
- **Server authorization/atomic decisions — PASS**: service gates every read/write and mutation audit shares the business transaction.
- **Feature-first layering — PASS**: each entity owns route/controller/service/repository/mapper/DTO files.
- **Model/contract discipline — PASS**: frozen schema fields, stable errors, decimal IDs, timestamps, and snake-case DTOs are preserved.
- **Focused verification/minimal change — PASS**: no schema, migration, `app.ts`, frontend, payroll, attendance, or employee-history edits.

### Post-Design Gate

The data model, contracts, and quickstart retain all pre-design guarantees. No
constitution violation or complexity exception is required.

## Technical Decisions

1. Repositories accept a root or transaction executor and are the only A2 files that query Drizzle.
2. Mutations read/lock the target in a service-owned transaction, write the row, then append a domain audit receipt before commit.
3. Services normalize A1 active grants into a visibility filter; self scope without A3 context returns no rows.
4. Child repositories validate active parents with joined persistence queries rather than importing another feature repository.
5. PostgreSQL unique violations become a stable internal duplicate signal and public `DUPLICATE_CODE`.
6. Branch timezones use the runtime IANA database and are persisted only after normalization.
7. Parent IDs exist on create and responses but are absent from update DTOs.
8. Deactivation does not cascade; effective usability requires an active record and active parent chain.

## Project Structure

### Documentation (this feature)

```text
specs/003-a2-organization/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/organization-api.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
backend/src/features/
├── shop/          # repository/service/controller/mapper/dto/validation/routes/tests
├── branch/        # same layered structure
├── department/    # same layered structure
├── position/      # same layered structure
└── organization/
    ├── organization.scope.ts
    ├── organization.errors.ts
    └── organization.*.test.ts
```

**Structure Decision**: Preserve existing entity feature folders. The small
`organization/` feature contains organization-domain coordination only and does
not become a repository-wide shared utility folder.

## Dependency and Delivery Order

```text
A1 actor/audit/errors → scoped-read foundation → shops
                                            ├→ branches → departments
                                            └→ positions
all resources → deactivation/completeness/integration
```

Shop is the first runnable slice. Branch and position may proceed in parallel
after shop contracts. Department follows branch. Routes remain independently
mountable for Person C.

## Complexity Tracking

No constitution violations require justification.
