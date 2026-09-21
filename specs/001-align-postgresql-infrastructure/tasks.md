# Tasks: Align PostgreSQL Infrastructure

**Input**: Design documents from `/specs/001-align-postgresql-infrastructure/`

**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md),
[research.md](./research.md), [data-model.md](./data-model.md), and
[database runtime contract](./contracts/database-runtime.md)

**Tests**: Required. The specification requires repeatable validation of dialect
consistency, clean migration, model preservation, failure safety, and development /
production parity. Use Bun's built-in test runner and the quickstart smoke checks.

**Organization**: Tasks are grouped by user story. Complete Phase 2 before starting
any user story work. `[P]` tasks edit independent paths and can be assigned to
different contributors after their listed dependencies are complete.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the versioned artifacts and safe configuration inputs needed
by all implementation work.

- [ ] T001 [P] Restore the canonical 36-table, 22-enum PostgreSQL model with documented relationship and enforcement notes in `haris-payroll-postgresql.dbml`
- [X] T002 [P] Add production-only variable placeholders and ignore the real secret file in `.env.production.example` and `.gitignore`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish one PostgreSQL schema, runtime, migration history, and test
baseline. No user story work begins until this phase is complete.

- [ ] T004 Replace `mysql2` with `pg` and add `@types/pg` while retaining the existing Drizzle versions in `backend/package.json` and `backend/bun.lock`
- [ ] T005 [P] Switch the canonical schema output to PostgreSQL migration history in `backend/drizzle.config.ts`
- [ ] T006 Add PostgreSQL-only URL validation that does not expose credentials in `backend/src/core/config/env.config.ts` and `backend/src/core/config/config.db.ts`
- [ ] T007 Create one pooled Drizzle `node-postgres` client with graceful shutdown ownership in `backend/src/core/db/client.ts`
- [ ] T008 Convert shared schema helpers and define all 22 named PostgreSQL enums in `backend/src/db/schema.columns.ts` and `backend/src/db/schema.enums.ts`; use `bigint` identity PKs/FKs, `date` strings, `timestamptz` events, `numeric(12,2)` money, and `numeric(8,2)` day/hour values
- [ ] T009 [P] Convert organization and access schemas from MySQL to PostgreSQL in `backend/src/features/shop/shop.schema.ts`, `backend/src/features/branch/branch.schema.ts`, `backend/src/features/department/department.schema.ts`, `backend/src/features/position/position.schema.ts`, `backend/src/features/role/role.schema.ts`, and `backend/src/features/user-account/user-account.schema.ts`
- [ ] T010 [P] Convert employee, assignment, bank-account, weekly-holiday, schedule, holiday-calendar, and attendance schemas in `backend/src/features/employee/employee.schema.ts`, `backend/src/features/employment-assignment/employment-assignment.schema.ts`, `backend/src/features/employee-bank-account/employee-bank-account.schema.ts`, `backend/src/features/employee-weekly-holiday/employee-weekly-holiday.schema.ts`, `backend/src/features/branch-schedule/branch-schedule.schema.ts`, `backend/src/features/holiday-calendar/holiday-calendar.schema.ts`, and `backend/src/features/attendance/attendance.schema.ts`
- [ ] T011 [P] Convert leave and overtime schemas in `backend/src/features/leave/leave.schema.ts` and `backend/src/features/overtime/overtime.schema.ts`
- [ ] T012 [P] Convert advance, loan, and debt schemas in `backend/src/features/advance/advance.schema.ts`, `backend/src/features/loan/loan.schema.ts`, and `backend/src/features/debt/debt.schema.ts`
- [ ] T013 [P] Convert payroll, payslip, attachment, and audit schemas in `backend/src/features/payroll/payroll.schema.ts`, `backend/src/features/payslip/payslip.schema.ts`, `backend/src/features/attachment/attachment.schema.ts`, and `backend/src/features/audit/audit.schema.ts`
- [ ] T014 Restore documented Drizzle relation metadata and export all converted tables/relations from `backend/src/db/schema.relations.ts` and `backend/src/db/schema.ts`
- [ ] T015 Regenerate the unused PostgreSQL initial migration and metadata, then retire the independent MySQL migration history in `backend/drizzle/`, `backend/drizzle/meta/`, and `backend/drizzle/mysql/`
- [ ] T016 Create the PostgreSQL catalog and URL-safety test harness in `backend/src/core/db/database.integration.test.ts` and replace the placeholder test command in `backend/package.json`
- [ ] T017 Verify the blocking baseline with `backend/drizzle.config.ts`, `backend/src/db/schema.ts`, and `backend/src/core/db/database.integration.test.ts`: typecheck passes, one clean migration creates 36 tables/22 enums, and no active MySQL dialect remains

**Checkpoint**: One canonical PostgreSQL schema and migration baseline exists. The
backend can reject MySQL URLs safely, and the user stories may begin.

---

## Phase 3: User Story 1 - Start a Consistent Development Environment (Priority: P1) 🎯 MVP

**Goal**: A developer can start the complete development stack from a clean checkout
without dialect mismatch or manual database repair.

**Independent Test**: Use the clean-stack and idempotence scenarios in
`specs/001-align-postgresql-infrastructure/quickstart.md`; migrations complete,
backend/frontend/gateway become healthy, and a stale MySQL URL fails without
credential leakage.

- [ ] T018 [P] [US1] Align development PostgreSQL variables, service wiring, health checks, and developer instructions in `.env.example`, `compose.yaml`, and `README.md`
- [ ] T019 [P] [US1] Replace backend-local MySQL workflow with root PostgreSQL convenience commands and documentation in `backend/package.json`, `backend/.env.example`, `backend/README.md`, and `backend/docker-compose.yaml`
- [ ] T020 [P] [US1] Add the watch-mode frontend container referenced by root Compose in `frontend/Dockerfile.dev` without changing frontend application code
- [ ] T021 [P] [US1] Align pre-server migration execution and non-secret error behavior in `backend/Dockerfile`, `backend/Dockerfile.dev`, and `backend/src/core/config/env.config.ts`
- [ ] T022 [US1] Extend the focused failure and catalog checks for PostgreSQL URLs, clean migration, stale MySQL guidance, and migration idempotence in `backend/src/core/db/database.integration.test.ts`
- [ ] T023 [US1] Execute and record the clean development-stack validation from `specs/001-align-postgresql-infrastructure/quickstart.md` against `.env.example`, `compose.yaml`, and `backend/drizzle/`, including elapsed time from `docker compose up --build -d` until all health checks pass; it MUST complete within 10 minutes

**Checkpoint**: A new contributor can boot the documented development stack in a
clean isolated environment and receives safe, actionable errors for invalid database
configuration.

---

## Phase 4: User Story 2 - Preserve the Payroll Domain Model (Priority: P2)

**Goal**: A maintainer can prove that PostgreSQL alignment preserves the approved
payroll model and its historical-data protections.

**Independent Test**: Run the catalog test against a clean migrated database and
compare `haris-payroll-postgresql.dbml`, Drizzle exports, and migration SQL: all 36
tables, 22 enums, relationships, critical constraints, and enforcement locations are
accounted for.

- [ ] T024 [P] [US2] Encode and document PostgreSQL-only exclusions, partial unique indexes, validation triggers, append-only triggers, locked-payroll immutability, and comments in `backend/drizzle/0000_*.sql` and `backend/drizzle/meta/`
- [ ] T025 [P] [US2] Add catalog assertions for the 36-table/22-enum inventory, `bigint` primary keys, `numeric(8,2)` day/hour values, foreign-key actions, relations, partial indexes, exclusions, and triggers in `backend/src/core/db/database.integration.test.ts`
- [ ] T026 [US2] Reconcile and correct parity across `haris-payroll-postgresql.dbml`, `haris-payroll-orm-reference.md`, `2026-09-10-haris-payroll-dbml-design.md`, `backend/src/db/schema.ts`, and `backend/drizzle/0000_*.sql`
- [ ] T027 [US2] Verify that append-only audit/approval/debt history and effective-dated assignment, holiday, schedule, and payroll-configuration protections remain enforceable in `backend/src/core/db/database.integration.test.ts` and `backend/drizzle/0000_*.sql`

**Checkpoint**: The canonical DBML, executable schema, and migration agree; no
payroll-domain entity or historical protection was silently weakened.

---

## Phase 5: User Story 3 - Maintain Development and Production Parity (Priority: P3)

**Goal**: A release operator can validate a production-like stack with the exact
PostgreSQL migration history used in development.

**Independent Test**: Start an isolated production-like Compose project with explicit
secrets and verify its schema catalog and migration history match the clean
development environment.

- [ ] T028 [P] [US3] Require explicit production database secrets and one PostgreSQL URL in `.env.production.example` and `compose.production.yaml`
- [ ] T029 [US3] Ensure the production backend image contains and applies the same canonical PostgreSQL migration path in `backend/Dockerfile`, `backend/drizzle/`, and `backend/drizzle.config.ts`
- [ ] T030 [US3] Add production-like catalog/parity assertions and no-credential-leak failure checks in `backend/src/core/db/database.integration.test.ts` and `specs/001-align-postgresql-infrastructure/quickstart.md`
- [ ] T031 [US3] Execute the production configuration and isolated-stack scenarios from `specs/001-align-postgresql-infrastructure/quickstart.md` using `compose.production.yaml` and `backend/drizzle/`

**Checkpoint**: Production-like startup requires explicit secrets and produces the
same PostgreSQL database model verified in development.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency review, documentation, and handoff without adding
business functionality.

- [ ] T032 [P] Update PostgreSQL-only setup, supported commands, legacy MySQL safety, and validation expectations in `README.md`, `backend/README.md`, and `specs/001-align-postgresql-infrastructure/quickstart.md`
- [ ] T033 [P] Review database-facing ignore rules and ensure no real environment secrets or generated local data are tracked in `.gitignore`, `backend/.gitignore`, and `.specify/.gitignore`
- [ ] T034 Run the complete final validation matrix from `specs/001-align-postgresql-infrastructure/quickstart.md`, attach results there, and review the feature diff to confirm it adds no business routes, controllers, services, repositories, API endpoints, or frontend UI changes
- [ ] T035 Coordinate commits within `backend/` and `frontend/`, then review repository status. Update root submodule pointers only after explicit owner approval

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1**: T001–T002 can begin immediately.
- **Phase 2**: T004–T017 depends on the setup decisions; T009–T013 begin after T008,
  T014 after T009–T013, T015 after T014, and T016–T017 after the migration baseline.
- **US1**: T018–T023 depends on T017. T018–T021 may run in parallel; T022 then T023
  validate their combined result.
- **US2**: T024–T027 depends on T015. T024 and T025 may run in parallel; T026 and
  T027 complete the parity review after both are done.
- **US3**: T028–T031 depends on T017, T021, and T027. T028 may run in parallel
  with completed US1 work; T029 begins after T021 and T027. T030 and T031 validate
  production parity.
- **Polish**: T032–T035 depends on US1, US2, and US3 completion.

### User Story Dependencies

```text
Setup → PostgreSQL foundation → US1 development startup
                         ├──→ US2 model preservation
                         └──→ US3 production parity (after US2 parity baseline)
US1 + US2 + US3 → Polish and team handoff
```

US1 is the MVP: it delivers a working, repeatable local PostgreSQL environment.
US2 prevents later payroll work from inheriting a weakened model. US3 extends the
same verified path to production-like deployment.

## Parallel Execution Examples

### Schema Conversion After T008

```text
Developer A: T009 organization and access schemas
Developer B: T010 employee, schedule, and attendance schemas
Developer C: T011 leave and overtime schemas
Developer D: T012 finance schemas
Developer E: T013 payroll, payslip, attachment, and audit schemas
```

### Development Environment After T017

```text
Developer A: T018 root development Compose and README
Developer B: T019 backend local environment, scripts, and README
Developer C: T020 frontend Dockerfile.dev
Developer D: T021 backend Docker startup and URL-safe configuration
```

### Model and Production Work

```text
Developer A: T024 manual PostgreSQL protections
Developer B: T025 database catalog assertions
Developer C: T028 production secrets and Compose
Developer D: T029 production image migration path
```

## Implementation Strategy

### MVP First (US1)

1. Complete T001–T017 to establish the canonical PostgreSQL foundation.
2. Complete T018–T023 and run the clean development-stack validation.
3. Stop and demonstrate that a fresh clone starts with PostgreSQL only before
   expanding the data-model or production validation work.

### Incremental Delivery

1. Foundation + US1: reliable developer onboarding and migration path.
2. US2: canonical DBML and verified historical-data safeguards.
3. US3: production-like environment parity with explicit secrets.
4. Polish: documentation, full validation evidence, and submodule handoff.

### Team Handoff

Work from the relevant submodule for backend or frontend changes. Do not run broad
cleanup or delete legacy volumes. T015 owns migration-history replacement; no other
task modifies `backend/drizzle/` until its owner completes the baseline. Root
submodule pointers require explicit owner approval.
