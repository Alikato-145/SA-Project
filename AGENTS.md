# Haris Payroll — Project Guide

## Purpose

Haris Payroll is a web system for a multi-branch restaurant. It replaces the
manual Excel-based process for employee records, attendance, leave, overtime,
employee debts, payroll, payslips, social-security reporting, and bank-transfer
exports. The primary users are employees, department supervisors, branch
managers, central HR/accounting, and owners.

Keep the system auditable: payroll and attendance data may be inspected later,
so preserve historical facts rather than silently overwriting or deleting them.

## Repository layout

- `frontend/` — Next.js 16, React 19, TypeScript, Tailwind CSS.
- `backend/` — Bun, Elysia, TypeScript.
- `frontend/AGENTS.md` — additional, mandatory instructions for frontend work.

`frontend/` and `backend/` are Git submodules. Work from the relevant
submodule when checking status, committing, or running its commands. Do not
update a submodule pointer unless the task explicitly requires it.

## Source of truth for the data model

The project’s planned PostgreSQL model is defined by these supplied reference
artifacts:

- `haris-payroll-postgresql.dbml` — tables, enums, references, and logical
  constraints.
- `haris-payroll-orm-reference.md` — domain meaning, ORM relation names, delete
  behavior, and implementation ordering.
- `2026-09-10-haris-payroll-dbml-design.md` — design decisions and critical
  constraints.

Do not casually rename, merge, or omit entities from that model. The Drizzle
schema is maintained separately; treat it as the executable schema and keep
application changes aligned with it. Discuss any schema mismatch with the
owner of that work before changing migrations or generated types.

## Domain map

`employees` is the central HR entity. `user_accounts` represents the actor who
performed an action, which may be an employee but is not interchangeable with
an employee record.

- Organization: shops, branches, departments, positions.
- Access control: user accounts, roles, scoped account roles.
- Employment history: assignments, salary/welfare history, bank accounts,
  weekly holidays.
- Operations: branch schedules, holidays, work-day records, leave, and OT.
- Finance: advances, loans/installments, and debt transactions.
- Payroll: configurations, periods, records, line items, adjustments, payslips,
  and delivery logs.
- Evidence: attachments and audit logs.

Use `snake_case` for database/API persistence fields and plural table names.
IDs are surrogate `bigint` primary keys. Store business dates as `date`, event
times as timezone-aware timestamps, and money as exact decimals—not floats.

## Non-negotiable business rules

- Pay is calculated daily. Absence and lateness are deductions; approved leave
  is not deducted. Keep deductions and non-deduction values visibly distinct.
- Preserve employment-assignment history. For a transfer, promotion, salary, or
  welfare change, end the prior effective-dated row and create a new one; never
  rewrite prior compensation history. Effective ranges for the same employee
  must not overlap.
- A work-day record is unique per employee and work date. Its branch is a
  historical snapshot, not a value derived later from the employee’s current
  assignment.
- Weekly holidays, branch schedules, and payroll configuration are
  effective-dated and must not have overlapping active ranges.
- Leave request days cannot overlap for an employee. Approval, quota use, and
  related attendance updates must be transactional. A supervisor can approve
  leave of up to three days; a branch manager can approve any request and may
  approve directly.
- Record every leave/OT decision as append-only approval history, including an
  approver’s correction to a requested leave type.
- OT is payable only when explicitly approved—never infer payable OT solely
  from a late clock-out. Support rest-day, hourly, and public-holiday OT.
- Advances require the configured eligibility checks: generally request date
  on/after the 20th, at least 20 worked days, and no more than half of base
  salary. Do not approve an advance that would make net pay negative after
  deductions.
- Loans are deducted by installment; food debt is transaction-based and its
  history is never reset or deleted.
- Social-security deductions use base salary only, excluding welfare.
- A payroll record is unique per employee per period. Locking a period requires
  complete attendance, no pending approvals, non-negative net pay, and a
  snapshot of all values used. Never edit locked payroll values; use a tracked
  payroll adjustment instead.
- A payslip belongs to exactly one payroll record. Email delivery attempts are
  logged individually. Enforce authorization so one employee cannot view or
  receive another employee’s payslip.

## Authorization and data safety

Apply role scope server-side—never rely on hidden frontend controls:

- Employee: own data only.
- Supervisor: own department.
- Branch manager: own branch.
- HR/accounting and owner: all branches, with duties appropriate to the role.

Roles describe a permission type; the account-role’s branch/department fields
provide its actual scope. Validate scope combinations. Avoid hard deletes for
master data or records that affect payroll history; prefer status fields and
append-only audit trails. Log sensitive changes with actor, action, target,
old/new values, and time. Never log passwords, hashes, tokens, or full bank
account details.

## Implementation expectations

- Keep business rules and authorization in backend services/routes, not only in
  UI validation.
- Use database transactions for multi-step approval, quota, deduction, payroll,
  and lock operations.
- Use explicit decimal handling for money; define rounding once in the payroll
  calculation layer and test it.
- Make APIs return stable error codes/messages for validation and state
  conflicts. UI should explain the business reason without exposing internals.
- Add focused tests for boundaries: leave at 3 vs. 4 days, quotas, schedule
  changes, date-20 advance eligibility, 20 worked days, half-salary caps,
  negative net pay, duplicate records, and locked-period adjustments.
- Before implementing an external time-clock integration or OCR, confirm scope:
  both are intentionally deferred. Keep time-entry sources replaceable.

## Backend architecture: feature-first layered design

Organize `backend/src/` by business feature first, then by layer. Do not create
one repository-wide `controllers/`, `services/`, or `repositories/` folder;
that mixes unrelated domains and makes feature ownership unclear.

```text
backend/src/
├── app.ts                         # Elysia composition only
├── index.ts                       # process startup only
├── core/                          # shared infrastructure, no business features
│   ├── config/
│   ├── db/
│   ├── errors/
│   ├── middleware/
│   └── auth/
├── shared/                        # small, domain-neutral utilities/types only
└── features/
    ├── employees/
    │   ├── employee.routes.ts
    │   ├── employee.controller.ts
    │   ├── employee.service.ts
    │   ├── employee.repository.ts
    │   ├── employee.mapper.ts
    │   ├── employee.dto.ts
    │   └── employee.schema.ts
    ├── attendance/
    ├── leave/
    ├── overtime/
    ├── advances/
    ├── loans/
    ├── debts/
    ├── payroll/
    └── reports/
```

Use a singular, feature-prefixed filename (`employee.service.ts`) so imports
remain unambiguous. Split a feature into subfolders only when it has enough
code to improve readability, for example `payroll/calculation/` or
`leave/approval/`; retain the same layer boundaries inside it.

### Permitted dependency flow

```text
Elysia route → controller → service → repository → database
                    │
                    └→ mapper → response DTO
```

- **Route layer** configures Elysia: HTTP method/path, hooks, authentication
  middleware, request validation schemas, and the controller handler. It must
  not contain business logic, database calls, or response conversion.
- **Controller layer** is the transport boundary. It extracts validated route
  inputs, performs request type/shape conversion into a service command, calls
  the service, and formats the HTTP response DTO. Controllers invoke mappers;
  no other layer converts database/domain data into response DTOs. Keep this
  layer thin and free from business decisions.
- **Mapper layer** contains pure, deterministic conversion functions such as
  `toEmployeeResponseDto`. Mappers do not query the database, call services, or
  enforce business rules. They are called only by controllers, so DTO formatting
  stays at the controller boundary.
- **Service layer** owns use-case orchestration and every business rule:
  authorization decisions, state transitions, calculations, effective-date
  checks, and transaction boundaries. Services use repositories and return
  domain/application data, never HTTP responses or response DTOs.
- **Repository layer** is the only feature layer that queries Drizzle/the
  database. It expresses persistence operations and query composition, but not
  business policy, DTO conversion, HTTP concerns, or Elysia types.

DTOs define the public request/response contracts. Keep request DTOs,
response DTOs, and service commands distinct when their shapes differ. Do not
return Drizzle rows directly from routes or services, even if they temporarily
look identical to an API response.

### Cross-feature work and shared code

- A feature may call another feature’s **service** through an explicit
  dependency; it must not import that feature’s repository or controller.
- Put reusable technical concerns in `core/` (database client, configuration,
  auth middleware, error translation) and only genuinely domain-neutral code
  in `shared/`. Do not move payroll or HR rules into `shared/` merely to avoid
  an import.
- Use a unit-of-work/transaction helper from `core/db` when one use case spans
  multiple repositories. The service owns the transaction, so approval and
  payroll operations remain atomic.
- Keep Drizzle schema and migrations in a clearly named database location
  decided with the schema owner (for example `backend/src/core/db/schema/` and
  `backend/drizzle/`). Repositories import the schema; controllers and routes
  do not.

### Naming and error handling

- Name service methods as use cases: `createEmployee`, `approveLeave`,
  `calculatePayrollPreview`, `lockPayrollPeriod`.
- Name repository methods after persistence intent: `findById`,
  `findForPayrollPeriod`, `insert`, `update`, `withTransaction`.
- Raise typed application errors in services/repositories. Translate them to
  status codes and public error DTOs in one Elysia error boundary/middleware;
  do not scatter HTTP status handling through services.
- A controller should map successful values with a mapper and let the shared
  error boundary map failures. Never expose password hashes, internal audit
  metadata, or full bank account numbers in response DTOs.

## Commands

Run commands in their own package directory using Bun:

```sh
cd frontend && bun run dev
cd frontend && bun run lint
cd frontend && bun run build
cd backend && bun run dev
```

The backend currently has no usable automated test script. Add appropriate test
commands as testing is introduced; do not treat the placeholder `bun test`/
`npm test` command as a passing check.

## Change discipline

- Read the nearest `AGENTS.md` before editing; nested instructions take
  precedence for their directory.
- Keep schema, migrations, API contracts, and UI terminology consistent.
- Do not alter historical payroll, approved attendance, approval history, or
  debt transactions through ordinary update flows.
- Update this guide when a confirmed architectural or domain decision changes.
