# A3 Data Model

The executable PostgreSQL tables and Drizzle schemas are existing assets. A3 does not add fields or migrations.

## Employee

`employees`: surrogate bigint ID, unique `employee_code` (30), unique nullable `national_id` (20), unique nullable `passport_id` (30), first/last name (100 each), phone (30), personal email (255), address, hire date, status (`active`, `inactive`, `suspended`, `terminated`), nullable termination date, timestamps.

- At least one national or passport ID is required.
- Termination date is null or on/after hire date.
- Employee status does not change login account status automatically.
- Full identity values are restricted to HR/Owner administration and never enter audit snapshots or team DTOs.

## Employment Assignment

`employment_assignments`: employee, branch, department, position IDs; employment type (`full_time`, `part_time`, `temporary`); `base_salary` and `welfare_amount` as `numeric(12,2)`; `effective_from`, nullable `effective_to`, `is_primary`, optional creating account, timestamps.

- Existing PostgreSQL exclusion constraint rejects overlapping inclusive ranges per employee.
- Department belongs to branch; position belongs to branch's shop; all masters must be active for a new assignment.
- Service-owned change ends the prior open range on the day before the new start and inserts a new row atomically.
- Historic rows, including old compensation, remain available for date-based queries.
- Money stays a decimal string in service and API contracts.

## Employee Bank Account

`employee_bank_accounts`: employee ID, bank code (20), bank name (100), holder name (200), account-number ciphertext, account-number last four, `is_primary`, `is_active`, timestamps.

- Ordinary response and audit contain only masked last four; plaintext never reaches persistence.
- Existing partial unique index permits at most one active primary per employee.
- Every insert supplies `is_primary` explicitly because the Drizzle/migration default differs from DBML.
- Primary switch and deactivation are transactional. Deactivation of a primary requires an active replacement or an explicit no-primary decision.
- Encrypted payload format remains versioned according to the key policy confirmed in research.

## Employee Weekly Holiday

`employee_weekly_holidays`: employee ID, weekday 0–6, effective start, nullable effective end, timestamps.

- Existing exclusion constraint rejects overlapping inclusive periods for one employee and weekday.
- Replacement closes the prior row before creating the new range; old rows remain readable.
- Date-based lookup is for downstream attendance/rest-day context.

## Related account and audit facts

`user_accounts.employee_id` is nullable and unique; account status is independent of employee status. A1 service owns account validation, creation, and temporary password handling. `audit_logs` remains append-only and stores one redacted outcome per public A3 action. The onboarding outcome summarizes its multiple domain changes in one allowlisted snapshot and commits with the business rows; it exposes no secrets.
