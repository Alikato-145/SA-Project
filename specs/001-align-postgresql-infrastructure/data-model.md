# Data Model: Align PostgreSQL Infrastructure

## Scope

This feature introduces no new business entities. It preserves and reconciles the
existing Haris Payroll model across DBML, Drizzle schema, and the canonical
PostgreSQL migration. The completed representations must agree on names, fields,
types, nullability, defaults, enums, relationships, delete/update behavior,
constraints, indexes, and historical-data protections.

## Preserved Domain Inventory

### Organization and Access

- `shops`
- `branches`
- `departments`
- `positions`
- `roles`
- `user_accounts`
- `user_account_roles`

### Employment History

- `employees`
- `employment_assignments`
- `employee_bank_accounts`
- `employee_weekly_holidays`

### Attendance and Scheduling

- `branch_schedules`
- `branch_schedule_overrides`
- `holiday_calendars`
- `work_day_records`

### Leave and Overtime

- `leave_types`
- `leave_requests`
- `leave_request_days`
- `leave_quotas`
- `leave_approval_actions`
- `overtime_records`
- `overtime_approval_actions`

### Employee Finance

- `advance_requests`
- `loans`
- `loan_installments`
- `debt_types`
- `debt_transactions`

### Payroll and Outputs

- `payroll_configurations`
- `payroll_periods`
- `payroll_records`
- `payroll_items`
- `payroll_adjustments`
- `payslips`
- `email_delivery_logs`

### Evidence

- `attachments`
- `audit_logs`

The expected baseline is 36 tables and 22 named PostgreSQL enum types.

## Canonical Type Mapping

| Domain value | PostgreSQL representation | Application representation | Validation |
|--------------|---------------------------|----------------------------|------------|
| Surrogate identifier | `bigint` identity | number until an API contract revisits ID serialization | Positive identity; all PK/FK pairs use the same SQL type |
| Small counters and calendar components | `smallint` or `integer` | number | Explicit bounds such as weekday `0..6` and month `1..12` |
| Business date | `date` | ISO `YYYY-MM-DD` string | No timezone conversion |
| Event instant | `timestamp with time zone` | `Date` | Millisecond precision where recorded |
| Clock time | `time` | string | Domain-specific ordering checks |
| Money | `numeric(12,2)` | decimal string | Non-negative/positive checks where required |
| Days or hours | `numeric(8,2)` | decimal string | Range and non-negative checks where required |
| Rate/config value | documented exact numeric precision | decimal string | Configuration-specific bounds |
| Audit snapshot | `jsonb` | structured JSON | Never stores credentials or full bank details |
| State/category | named PostgreSQL enum | string union | Exactly the 22 documented enum value sets |

Using number mode for SQL `bigint` preserves the current TypeScript surface but is
safe only below JavaScript's maximum safe integer. Public API ID serialization must
be decided before IDs can approach that bound; this feature does not introduce an
API contract.

## Relationships

All foreign keys and delete/update actions described in
`haris-payroll-orm-reference.md` are preserved. Drizzle relation metadata is restored
with the documented semantic names, including distinct actor relations such as
submitted, approved, calculated, locked, generated, and voided actions.

Key relationship rules include:

- `employees` and `user_accounts` are distinct concepts with an optional one-to-one
  link.
- employment, schedule, holiday, and configuration rows retain effective dates.
- `work_day_records.branch_id` remains a historical branch snapshot.
- `payroll_records` retain assignment and monetary snapshots for their period.
- payslips remain one-to-one with payroll records; delivery attempts remain
  one-to-many and append-only.
- debt reversals retain their link to the original transaction.

## Required Database Protections

### Uniqueness

- one work-day record per employee/date;
- one overtime record per employee/date;
- one leave quota per employee/type/year;
- one payroll record per employee/period;
- one payslip per payroll record;
- one branch schedule override per branch/date;
- scoped account-role grants remain unique even when scope columns are null;
- one active primary bank account per employee.

### Temporal Exclusion

Active ranges cannot overlap for the same applicable scope in employment
assignments, employee weekly holidays, branch schedules, and payroll configurations.
Approved leave dates cannot overlap for one employee.

### Validation Triggers

- account-role branch/department values must match the role scope;
- assignment department and position must belong to the selected branch/shop;
- attachment ownership is exactly one supported owner type;
- state-specific timestamps and references remain internally consistent.

### Historical Immutability

Database triggers reject update/delete operations on audit logs, leave approval
actions, overtime approval actions, and debt transactions. Locked payroll values
reject direct mutation; corrections use payroll adjustments.

## State Transitions

This alignment does not change business state machines. It preserves the existing
enum values and validates that transitions remain enforceable by future services:

- leave and overtime: pending decisions remain distinct from approved/rejected and
  append every approval action;
- advance: pending → approved/rejected/cancelled → deducted where applicable;
- loan installments: scheduled → deducted/waived/cancelled;
- payroll period: draft → previewed → locked;
- payroll record: draft → calculated → locked;
- payroll adjustment: pending → approved/rejected → applied;
- payslip: generated → voided.

## Baseline Reconciliation

Before accepting the regenerated migration:

1. DBML, Drizzle exports, and migration must each contain all 36 tables.
2. Drizzle enum declarations and migration must contain all 22 enums with identical
   values and ordering.
3. Every documented relation, unique rule, FK action, check, partial index,
   exclusion constraint, trigger, and comment must have a recorded representation.
4. `roles`, `leave_types`, and `debt_types` must use `bigint`, not the prior
   `smallint` representation.
5. All day/hour values must use `numeric(8,2)`, replacing prior mixed precision.
6. Generated migration output must be reviewed before the independent MySQL history
   is removed from the supported tree.

