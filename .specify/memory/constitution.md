<!--
Sync Impact Report
- Version change: 1.0.0 → 1.0.1
- Modified principle: IV, confirmed PostgreSQL baseline (clarification only)
- Added sections: Core Principles, Domain-Specific Constraints,
  Development Workflow and Quality Gates, Governance
- Removed sections: none
- 2026-09-22 clarification: PostgreSQL 16 is the confirmed sprint database;
  feature schemas and backend/drizzle/ are frozen under the schema owner.
-->

# Haris Payroll Constitution

## Core Principles

### I. Historical Payroll Integrity

Payroll, attendance, approved leave and OT decisions, debt transactions, and
employment compensation history MUST be preserved as auditable historical facts.
Locked payroll values MUST NOT be edited; corrections use tracked adjustments.
Transfers, promotions, salary, welfare, schedules, and weekly holidays MUST be
represented by new effective-dated records, with prior records closed rather than
rewritten. This preserves the factual basis for every past payslip and report.

### II. Server-Enforced Authorization and Atomic Decisions

The backend MUST enforce role scope for every protected action; hidden frontend
controls are never an authorization boundary. Employee access is limited to owned
data, supervisors to their department, branch managers to their branch, and HR,
accounting, and owners to authorized all-branch duties. Leave approval, quota use,
attendance effects, deductions, and payroll locking MUST use transactions whenever
their state changes span multiple records. Sensitive changes MUST create an audit
record without storing passwords, tokens, hashes, or full bank account numbers.

### III. Feature-First Layered Backend

Backend code MUST be organized by business feature. Dependencies flow only from
Elysia route to controller to service to repository to database; controllers may
invoke pure mappers for response DTOs. Services own business rules, calculations,
authorization, state transitions, and transaction boundaries. Repositories are the
only feature-layer code that queries Drizzle. Cross-feature access MUST use an
explicit service dependency, never another feature's repository or controller.

### IV. Data Model and Contract Discipline

The supplied PostgreSQL DBML and ORM reference define the intended domain model;
the Drizzle schema is the executable schema and application contracts MUST remain
aligned with both. Persistence fields use `snake_case`, plural table names,
`bigint` surrogate IDs, `date` business dates, timezone-aware event timestamps,
and exact decimals for money. PostgreSQL 16 is the confirmed database for the
two-week sprint. Feature-owned Drizzle schemas and `backend/drizzle/` are the canonical, frozen baseline; schema
changes require coordination with the schema owner. No feature may use a
conflicting database dialect or migration path. API errors MUST expose stable public
codes and messages without leaking internals.

### V. Focused Verification and Minimal Change

Every change MUST be limited to the requested scope and follow the existing
architecture unless a documented decision changes it. Business-rule changes MUST
add focused tests for relevant boundaries, especially approval limits, effective
date overlaps, eligibility thresholds, duplicate records, non-negative net pay,
and locked-period adjustments. The placeholder backend test script is not evidence
of a passing test suite. External time-clock integration and OCR remain deferred
until explicitly approved.

## Domain-Specific Constraints

Daily pay calculation MUST distinguish deductible absence and lateness from
approved leave. Payable OT MUST require explicit approval and support rest-day,
hourly, and public-holiday types. Social-security deductions use base salary only,
excluding welfare. Advances require the configured date, worked-day, salary-cap,
and non-negative-net-pay checks. Loans are deducted by installment; food-debt
transactions are append-only.

Each employee has at most one work-day record per work date and one payroll record
per payroll period. Leave request dates cannot overlap for an employee. Weekly
holidays, branch schedules, payroll configuration, and employment assignments
cannot have overlapping active effective ranges. A payroll period may lock only
after attendance is complete, approvals are resolved, net pay is non-negative, and
the calculation inputs are snapshotted. A payslip belongs to exactly one payroll
record, and every delivery attempt is logged.

## Development Workflow and Quality Gates

Work begins with a feature specification, then a technical plan and dependency-
ordered tasks before implementation. Each feature change MUST identify affected
domain rules, authorization scope, transaction boundaries, API contracts, schema
impact, and focused verification. Reviewers MUST verify compliance with this
constitution and the nearest applicable `AGENTS.md`.

Frontend work follows the frontend-specific instructions. Backend work runs from
the `backend/` submodule and frontend work from the `frontend/` submodule; commits
and status checks MUST be performed in the relevant submodule. A task MUST NOT
update a submodule pointer unless that update is explicitly requested.

## Governance

This constitution governs implementation choices in Haris Payroll. `AGENTS.md`,
the DBML design, the ORM reference, and feature specifications provide supporting
guidance; when they conflict, the project owner MUST resolve the conflict before
implementation rather than silently choosing an interpretation.

Amendments require a documented rationale, an impact review for schema, API,
historical data, and tests, and an update to this file. Backward-incompatible
principle removals or redefinitions require a MAJOR version bump; new principles
or materially expanded requirements require MINOR; clarifications require PATCH.
Every review and implementation plan MUST include a constitution compliance check.

**Version**: 1.0.1 | **Ratified**: 2026-09-21 | **Last Amended**: 2026-09-22
