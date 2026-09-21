# Feature Specification: Align PostgreSQL Infrastructure

**Feature Branch**: `not-created`

**Created**: 2026-09-21

**Status**: Draft

**Input**: User description: "Align the Haris Payroll database infrastructure to
PostgreSQL so that the Drizzle schema, migrations, environment configuration,
Docker development stack, and production stack use one consistent database
dialect. Preserve the existing domain model and do not implement business feature
APIs yet."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start a Consistent Development Environment (Priority: P1)

As a developer, I can start Haris Payroll from a clean checkout using the
documented development workflow without encountering a database dialect or
connection-string mismatch.

**Why this priority**: Every later feature depends on a working database and a
repeatable local environment. The current mismatch blocks reliable development.

**Independent Test**: Start from an empty development database, follow the
documented setup workflow, and verify that migrations complete and the backend
becomes healthy without manual database configuration changes.

**Acceptance Scenarios**:

1. **Given** a clean checkout and an empty database volume, **When** a developer
   starts the development stack using the documented command, **Then** the database
   is initialized successfully and all application health checks pass.
2. **Given** the provided environment example, **When** a developer configures the
   backend, **Then** every database setting describes the same PostgreSQL target and
   no MySQL-specific setting is required.
3. **Given** a database connection failure, **When** the backend starts, **Then** the
   failure identifies the invalid or unavailable database configuration without
   exposing credentials.

---

### User Story 2 - Preserve the Payroll Domain Model (Priority: P2)

As a project maintainer, I can verify that aligning the infrastructure does not
remove, rename, merge, or weaken any existing payroll-domain entity, relationship,
constraint, enum, or historical-data rule.

**Why this priority**: The database represents auditable payroll facts. A dialect
alignment is unacceptable if it silently changes the approved business model.

**Independent Test**: Compare the aligned database definition with the supplied
PostgreSQL model references and verify that every entity and critical constraint
has either an equivalent representation or an explicitly documented enforcement
location.

**Acceptance Scenarios**:

1. **Given** the supplied PostgreSQL data-model references, **When** the aligned
   schema is reviewed, **Then** all existing domain entities, fields, enums,
   relationships, uniqueness rules, and delete behaviors remain represented.
2. **Given** a rule that cannot be expressed directly in the schema definition,
   **When** the alignment is reviewed, **Then** its required enforcement location is
   explicitly documented and the rule is not silently omitted.
3. **Given** payroll and employment history requirements, **When** migrations are
   applied, **Then** append-only and effective-dated data remains distinguishable
   from mutable operational data.

---

### User Story 3 - Maintain Development and Production Parity (Priority: P3)

As a release operator, I can deploy the production stack using the same database
dialect and migration history validated in development.

**Why this priority**: Production must not introduce a second database behavior or
migration path after a feature has passed development validation.

**Independent Test**: Initialize both clean development and production-like
environments and verify that each reaches a healthy state from the same ordered
migration history with no environment-specific schema edits.

**Acceptance Scenarios**:

1. **Given** clean development and production-like databases, **When** each stack is
   initialized, **Then** both apply the same ordered migration history successfully.
2. **Given** a future schema change, **When** a maintainer generates and reviews a
   migration, **Then** only the supported PostgreSQL migration path is produced.
3. **Given** legacy MySQL-specific configuration or generated artifacts, **When** the
   repository is validated, **Then** none are used by supported development,
   validation, or production workflows.

### Edge Cases

- A developer has a pre-existing MySQL development volume or local environment
  file from the previous setup.
- A PostgreSQL migration already exists while generated metadata reflects another
  dialect or migration history.
- A domain constraint has different semantics or is unsupported by the previous
  schema representation.
- Migration execution is interrupted after only part of the migration history is
  applied.
- Environment variables are missing, malformed, or contain credentials that must
  not appear in logs.
- A proposed alignment change attempts to add business routes, services, or UI
  outside this feature's scope.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: All supported development, validation, and production database
  workflows MUST identify PostgreSQL as the single database dialect.
- **FR-002**: A clean database MUST be fully initialized through the documented
  migration workflow without manual schema changes.
- **FR-003**: Development and production-like environments MUST apply the same
  ordered migration history and produce equivalent database structures.
- **FR-004**: The aligned model MUST preserve every existing business entity,
  relationship, enum, field, uniqueness rule, delete behavior, and auditable-history
  requirement defined by the approved model references.
- **FR-005**: Any cross-row, temporal, or transactional rule that cannot be enforced
  directly by the database definition MUST have its enforcement responsibility
  recorded without weakening the rule.
- **FR-006**: Supported environment examples and startup workflows MUST use
  consistent database names, ports, credentials placeholders, and connection
  targets, with no real credentials committed.
- **FR-007**: Unsupported MySQL-specific configuration and generated artifacts MUST
  not participate in any supported workflow after alignment.
- **FR-008**: A stale MySQL development environment MUST fail with actionable
  migration guidance rather than being silently treated as PostgreSQL or deleted.
- **FR-009**: Startup and migration failures MUST report the failing configuration
  category or migration step without exposing database credentials.
- **FR-010**: This feature MUST NOT introduce employee, attendance, leave, overtime,
  finance, payroll, payslip, reporting, or other business-feature APIs.
- **FR-011**: The repository MUST provide a repeatable validation procedure covering
  clean initialization, migration completion, backend health, and dialect
  consistency.
- **FR-012**: Existing historical-data protections MUST remain intact; alignment
  MUST NOT require destructive rewriting of payroll, attendance, approval, debt, or
  employment history.

### Key Entities

- **Domain Model Baseline**: The approved collection of payroll-domain entities,
  relationships, constraints, enums, and delete behaviors that must remain
  unchanged by infrastructure alignment.
- **Migration History**: The ordered, repeatable set of database changes used to
  create and evolve the database consistently in every supported environment.
- **Runtime Database Configuration**: The environment-specific connection settings
  consumed by development and production-like workflows without changing dialect.
- **Environment Instance**: A clean or existing database runtime whose health,
  migration state, and compatibility can be validated.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new contributor can initialize the complete development environment
  from a clean checkout in 10 minutes or less using only the documented steps.
- **SC-002**: Clean development and production-like initialization complete with
  100% of migrations applied and all configured health checks passing.
- **SC-003**: Repository validation finds zero active mixed-dialect settings or
  supported MySQL migration paths.
- **SC-004**: A model comparison accounts for 100% of existing domain entities and
  critical constraints, with zero unapproved removals or semantic changes.
- **SC-005**: Repeating clean initialization twice produces equivalent database
  structures with no manual intervention.
- **SC-006**: Review confirms zero new business-feature API endpoints or UI flows in
  the alignment change.

## Assumptions

- PostgreSQL is the confirmed target because the approved model references and both
  supported application stacks already identify it as the intended database.
- Current local MySQL data is development-only unless a maintainer explicitly
  identifies data that requires a separate migration plan; no existing data may be
  deleted automatically.
- The approved DBML, ORM reference, and design-decision document remain the source
  of truth for domain semantics during alignment.
- This feature may change database definitions, migration metadata, environment
  examples, startup configuration, and validation documentation, but not business
  behavior or public business APIs.
- Authentication, authorization workflows, and feature-specific database access
  remain outside this feature except where required to confirm that existing model
  structures were preserved.

