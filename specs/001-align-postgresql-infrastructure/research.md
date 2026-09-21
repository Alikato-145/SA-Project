# Research: Align PostgreSQL Infrastructure

## PostgreSQL Runtime Driver

**Decision**: Replace `mysql2` with `pg` and use one `pg.Pool` through
`drizzle-orm/node-postgres`.

**Rationale**: The adapter works with the repository's installed Drizzle line and
provides mature pooling, transaction, and type-parser behavior. Keeping Drizzle at
its current version isolates the dialect change from an unrelated dependency
upgrade. This matters for payroll dates, timestamps, bigint identifiers, and exact
decimals.

**Alternatives considered**:

- Bun SQL would remove one dependency, but the installed Drizzle line predates
  relevant date/timestamp mapping fixes. Reconsider it in a separate Drizzle upgrade.
- Postgres.js is supported but adds a dependency just like `pg` and its default
  prepared statements may require deployment-specific configuration with a pooler.

**References**:

- [Drizzle PostgreSQL drivers](https://orm.drizzle.team/docs/get-started-postgresql)
- [Drizzle with Bun and PostgreSQL](https://orm.drizzle.team/docs/tutorials/bun-railway-pg)
- [node-postgres pooling](https://node-postgres.com/features/pooling)
- [node-postgres transactions](https://node-postgres.com/features/transactions)

## PostgreSQL Type Mapping

**Decision**: Use `pgTable`, 22 named `pgEnum` definitions, PostgreSQL identity
columns, `date` values represented as strings, timezone-aware timestamps represented
as dates, exact `numeric` values represented without floating-point conversion, and
`jsonb` for audit snapshots.

All surrogate primary keys and their foreign keys use SQL `bigint`, including
`roles`, `leave_types`, and `debt_types`. Day/hour quantities use `numeric(8,2)`.
These decisions follow the project guide and design document, as confirmed by the
owner, even where the unused executable baseline previously differed.

**Rationale**: The mapping preserves calendar dates independently of process
timezone, preserves event instants, and prevents precision loss in payroll values.
PostgreSQL has no unsigned integer type, so non-negative rules remain explicit
checks where the domain requires them.

**Alternatives considered**:

- Preserving `smallint` master IDs and mixed decimal precision was rejected because
  it conflicts with the confirmed source-of-truth rules.
- Mapping exact monetary values to JavaScript numbers was rejected because binary
  floating point cannot preserve all decimal values exactly.

**References**:

- [Drizzle PostgreSQL column types](https://orm.drizzle.team/docs/column-types/pg)
- [node-postgres data types](https://node-postgres.com/features/types)

## Canonical Model and Missing DBML

**Decision**: Reconstruct `haris-payroll-postgresql.dbml` from
`haris-payroll-orm-reference.md`, `2026-09-10-haris-payroll-dbml-design.md`, and the
existing PostgreSQL migration, then cross-check all three representations before
accepting the new baseline.

**Rationale**: The guide names the DBML as a source of truth, but the file is absent.
The inspectable MySQL and PostgreSQL snapshots each contain the same 36 tables and
column sets, and the PostgreSQL snapshot contains the expected 22 named enums. The
reference documents supply domain semantics that generated SQL cannot express.

**Alternatives considered**:

- Treating the MySQL schema as authoritative was rejected because PostgreSQL is the
  confirmed target and MySQL cannot represent all required temporal protections.
- Continuing without DBML was rejected because future model reviews would lack the
  declared canonical artifact.

## Migration History

**Decision**: Regenerate a single PostgreSQL initial migration in
`backend/drizzle/` after schema and DBML parity is established. Port the required
manual PostgreSQL protections into that baseline. Remove `backend/drizzle/mysql/`
from supported artifacts after validation.

**Rationale**: The owner confirmed that the existing `0000` migration has never
been applied to a shared, staging, or production database. Regeneration avoids a
noisy follow-up migration solely to correct an unused baseline while retaining Git
history for recovery.

**Alternatives considered**:

- Keeping the old PostgreSQL `0000` and adding `0001` was rejected because no
  deployed database depends on it and the old baseline conflicts with confirmed
  ID and decimal rules.
- Translating or interleaving the MySQL `0000` was rejected because it is an
  independent migration history with incompatible metadata.
- `db:push` is not a supported workflow because it bypasses reviewed ordered
  migrations.

## PostgreSQL-Only Protections

**Decision**: Preserve and test the manual protections that portable schema
generation does not fully express:

- `btree_gist` support and exclusion constraints for employment assignments,
  branch schedules, payroll configurations, approved leave dates, and weekly
  holidays;
- partial unique indexes for scoped account roles and active primary bank accounts;
- scope and assignment-consistency validation triggers;
- append-only triggers for audit logs, leave approval actions, overtime approval
  actions, and debt transactions;
- locked payroll immutability enforced by a database trigger, with future service
  checks acting as a second boundary;
- schema comments that identify historical snapshots and sensitive fields.

**Rationale**: These rules protect auditable history and cross-row invariants. Their
enforcement cannot be inferred from table count or foreign keys alone.

**Alternatives considered**:

- Deferring all protections to future services was rejected because infrastructure
  alignment must not weaken the existing model and some rules protect data from
  every write path.

## Relations Metadata

**Decision**: Restore Drizzle `relations()` metadata in one
`backend/src/db/schema.relations.ts` file and export it from the schema entry point.

**Rationale**: Physical foreign keys exist, but the feature-split MySQL source lost
the relation metadata and names described by the ORM reference. A centralized file
preserves feature table ownership while avoiding cross-feature schema cycles.

**Alternatives considered**:

- Omitting relations was rejected because the feature requires relationship parity.
- Distributing cross-feature relations across every feature was rejected because it
  increases cycles and touches more files without improving ownership.

## Runtime and Container Workflow

**Decision**: Root `compose.yaml` and `compose.production.yaml` remain canonical.
Both wait for PostgreSQL health, and both backend images run the same ordered
migration command before starting the server. Backend convenience scripts target
the root PostgreSQL service; the backend-local MySQL Compose file is retired.

**Rationale**: This preserves the project's current single-process startup model and
requires fewer moving parts than a separate migration service. If production later
runs multiple backend replicas, migration must move to a one-shot release job before
scaling.

**Alternatives considered**:

- A dedicated migration service was deferred because the current deployment has one
  backend process and does not need replica coordination yet.
- Keeping a second backend-local Compose stack was rejected because it duplicates
  configuration and caused the current dialect split.

## Configuration and Legacy Safety

**Decision**: Accept only `postgres:` and `postgresql:` database URLs. Development
examples may contain disposable local credentials; production Compose requires an
explicit secret URL and has no default password. Errors identify the invalid
configuration category without printing the URL.

Legacy MySQL configuration fails fast with migration guidance. Old MySQL volumes
are never deleted or converted automatically; real data export/import is a separate
feature if later required.

**Rationale**: Protocol validation prevents the same mixed-dialect failure from
returning. Explicit production secrets avoid insecure defaults and URL interpolation
failures with reserved password characters.

**Alternatives considered**:

- Accepting any non-empty URL was rejected because it allows configuration to drift
  back to MySQL.
- Automatically deleting or converting legacy data was rejected because data
  ownership and recoverability are not established.

## Full Development Stack

**Decision**: Add the missing `frontend/Dockerfile.dev` as a minimal development
container so the already documented root Compose workflow can be validated end to
end. No frontend application code changes.

**Rationale**: The existing development Compose file references this file, so a
clean checkout cannot currently satisfy the feature's primary acceptance scenario.

**Alternatives considered**:

- Narrowing validation to PostgreSQL and backend only was rejected because the
  specification explicitly promises a complete development environment.
