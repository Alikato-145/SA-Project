# Implementation Plan: Align PostgreSQL Infrastructure

**Branch**: `001-align-postgresql-infrastructure` | **Date**: 2026-09-21 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from
`/specs/001-align-postgresql-infrastructure/spec.md`

## Summary

Replace the active MySQL Drizzle path with one PostgreSQL 16 path shared by local,
containerized development, and production. Reconstruct the missing canonical DBML,
convert the feature-owned schemas to PostgreSQL types, regenerate the unused initial
migration, and keep the business model intact. Use `pg` with Drizzle's
`node-postgres` adapter, retain the installed Drizzle versions, and add only the
smallest runtime client and database integration check needed for future features.
No business routes, services, repositories, or UI behavior are introduced.

## Technical Context

**Language/Version**: TypeScript 5.9 on Bun 1.3.11

**Primary Dependencies**: Elysia, Drizzle ORM 0.44.x, Drizzle Kit 0.31.x,
`pg`, `@types/pg`, Zod, dotenv, Docker Compose

**Storage**: PostgreSQL 16; one canonical migration history in `backend/drizzle/`

**Testing**: Bun's built-in test runner, TypeScript `tsc --noEmit`, Drizzle
generation/migration checks, PostgreSQL catalog assertions, and Docker Compose
smoke tests

**Target Platform**: Bun backend in Alpine Linux containers; local development on
Docker Desktop or Docker Engine; PostgreSQL 16 in development and production

**Project Type**: Web application with root orchestration and independent backend
and frontend Git submodules

**Performance Goals**: Clean checkout reaches a healthy development stack within
10 minutes; repeated migration runs add no duplicate objects or migration entries

**Constraints**: Preserve 36 domain tables, 22 enum types, documented relationships,
PostgreSQL-only constraints/triggers, exact decimal values, business dates, and
timezone-aware event timestamps. Never log credentials or automatically delete
legacy MySQL data. Do not add business APIs or upgrade Drizzle in this feature.

**Scale/Scope**: Root environment and Compose configuration, two backend container
images, 20 feature schema modules plus shared schema files, one runtime database
client, one integration test, one restored DBML artifact, and one minimal frontend
development Dockerfile needed by the existing root stack

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate

| Principle | Result | Evidence |
|-----------|--------|----------|
| Historical payroll integrity | PASS | Owner confirmed the existing initial migration has never been used in shared, staging, or production environments; no data is migrated or deleted automatically. |
| Server-enforced authorization and atomic decisions | PASS | Authorization and business transactions are outside scope; database transaction support is prepared without adding policy. |
| Feature-first layered backend | PASS | Feature schema ownership remains unchanged; shared connection and schema helpers stay in database infrastructure. |
| Data model and contract discipline | PASS | PostgreSQL is the single dialect, documented `bigint` and `numeric(8,2)` rules win confirmed conflicts, and DBML restoration is required. |
| Focused verification and minimal change | PASS | Existing Drizzle versions remain; one mature driver replaces `mysql2`; tests target only schema/configuration behavior. |
| Domain-specific constraints | PASS | Manual PostgreSQL exclusions, partial indexes, validation triggers, append-only triggers, and enforcement-location notes are preserved. |
| Workflow and submodule discipline | PASS | Work is planned per real repository path; backend/frontend commits and root pointer updates must be coordinated explicitly during implementation. |

No constitution violations require justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-align-postgresql-infrastructure/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── database-runtime.md
└── tasks.md                  # Created later by $speckit-tasks
```

### Source Code (repository root)

```text
./
├── .env.example
├── .env.production.example          # new: placeholders only
├── README.md
├── compose.yaml
├── compose.production.yaml
├── haris-payroll-postgresql.dbml    # restored canonical model
├── backend/                         # Git submodule
│   ├── .env.example
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── README.md
│   ├── bun.lock
│   ├── drizzle.config.ts
│   ├── drizzle/
│   │   ├── 0000_<generated>.sql     # regenerated unused PostgreSQL baseline
│   │   └── meta/
│   ├── package.json
│   └── src/
│       ├── core/
│       │   ├── config/
│       │   │   ├── config.db.ts
│       │   │   └── env.config.ts
│       │   └── db/
│       │       ├── client.ts
│       │       └── database.integration.test.ts
│       ├── db/
│       │   ├── schema.columns.ts
│       │   ├── schema.enums.ts
│       │   ├── schema.relations.ts
│       │   └── schema.ts
│       └── features/*/*.schema.ts
└── frontend/                        # Git submodule
    └── Dockerfile.dev               # new: restores documented dev stack
```

The obsolete `backend/docker-compose.yaml` and `backend/drizzle/mysql/` paths are
retired after their content is verified against the PostgreSQL baseline. Git
history is the recovery path; legacy local volumes are never removed automatically.

**Structure Decision**: Preserve feature-owned table definitions in
`backend/src/features/` and keep `backend/src/db/schema.ts` as the Drizzle Kit entry
point. Put the shared runtime client under `backend/src/core/db/` and centralize
Drizzle relation metadata in `backend/src/db/schema.relations.ts` to avoid moving
feature tables or creating cross-feature repository imports. Root Compose remains
the only container orchestration source.

## Phase 0: Research Decisions

Research is consolidated in [research.md](./research.md). All technical unknowns
are resolved: PostgreSQL 16 is the only dialect, `pg` is the runtime driver, the
unused initial migration may be regenerated, documentation rules resolve type
conflicts, and legacy MySQL data is explicitly outside automatic migration.

## Phase 1: Design

1. Restore `haris-payroll-postgresql.dbml` from the ORM reference, design document,
   and verified 36-table PostgreSQL baseline. Review it before schema generation.
2. Convert shared columns, named enums, feature tables, relations, constraints, and
   PostgreSQL-only manual protections according to [data-model.md](./data-model.md).
3. Replace `mysql2` with `pg`, add one pooled Drizzle client, validate only
   PostgreSQL URLs, and keep credentials out of errors.
4. Regenerate one canonical initial migration because the owner confirmed the old
   initial migration was never shared or deployed. Remove the independent MySQL
   migration history only after parity checks pass.
5. Align root/backend environment examples, scripts, Dockerfiles, Compose files,
   and documentation with [database-runtime.md](./contracts/database-runtime.md).
6. Add the missing frontend development Dockerfile required by the existing root
   Compose workflow; do not alter application UI code.
7. Run the validation scenarios in [quickstart.md](./quickstart.md), including
   clean initialization, catalog counts, manual constraint checks, idempotence,
   failure safety, and production parity.

### Post-Design Constitution Check

All pre-design gates remain PASS. The design adds no business behavior, does not
weaken historical protections, keeps exact money and date semantics, records all
non-schema enforcement locations, uses one driver and migration path, and includes
focused automated and end-to-end validation. No complexity exception is required.
