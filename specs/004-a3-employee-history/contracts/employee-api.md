# A3 Employee API Contract

## Common conventions

- Base path `/api/v1`; JSON fields use `snake_case`.
- IDs are canonical positive decimal strings within the current safe-number driver range. Business dates use `YYYY-MM-DD`; money uses exact two-decimal strings.
- List responses: `{ data, page, page_size, total, request_id }`; detail/mutation responses: `{ data, request_id }`.
- Errors use `{ error: { code, message, field_errors? }, request_id }`.
- Mutations require the existing A1 cookie, allowed Origin, and JSON content type. Authorization is enforced in services.
- No employee, assignment, bank, or holiday `DELETE` method is public.

## Field visibility

| Actor | Employee list/detail | Assignment and pay | Bank |
|---|---|---|---|
| Employee | Own safe profile | Own non-financial assignment summary | Own masked accounts |
| Supervisor | Current department's basic team fields | No compensation history | None |
| Branch manager | Current branch's basic team fields | No compensation history | None |
| HR | All branches, full HR fields | All authorized history | Masked account metadata |
| Owner | All branches, full HR fields | All authorized history | Masked account metadata |

Basic team fields: `id`, `employee_code`, `first_name`, `last_name`, current `branch_id`, `department_id`, `position_id`, employee `status`. Full HR fields additionally include contact details, `hire_date`, `terminated_at`, and presence/masked display of identity identifiers. Ordinary responses never contain full national/passport values. If HR workflows need full values for edits, they send replacements without a full-value GET.

## Employee master

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/employees` | Scoped search/list; `page`, `page_size`, `search`, `status`, `branch_id`, `department_id` |
| `POST` | `/employees` | Create employee identity (HR/Owner) |
| `GET` | `/employees/:employee_id` | Safe scoped detail |
| `PATCH` | `/employees/:employee_id` | Update safe identity/contact fields (HR/Owner) |
| `PATCH` | `/employees/:employee_id/status` | Change employee status with reason and optional termination date (HR/Owner) |
| `POST` | `/employees/onboard` | Atomic employee + first assignment + selected options |

Create requires `employee_code`, `first_name`, `last_name`, `hire_date`, and at least one of `national_id` or `passport_id`. Optional fields are phone, personal email, and address. Update cannot change immutable employee code or historical hire date without a separately specified correction flow. Identity replacement is validated for uniqueness. Status is one of `active`, `inactive`, `suspended`, `terminated`; termination requires a date on/after hire date. Employee status never implicitly changes account status.

`POST /employees/onboard` body nests `employee`, `assignment`, optional `bank_account`, `weekly_holidays[]`, and optional `account` (username). Its successful response contains safe employee and created resource IDs. If an account is selected, `temporary_password` appears only in this response; when no account is selected, the field is omitted.

## Assignment history

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/employees/:employee_id/assignments` | HR/Owner history; own/team sees only non-financial current summary via employee detail |
| `POST` | `/employees/:employee_id/assignments` | Initial assignment or effective-dated change (HR/Owner) |

Input: `branch_id`, `department_id`, `position_id`, `employment_type`, `base_salary`, `welfare_amount`, `effective_from`; an optional `effective_to` is allowed only for an explicitly bounded initial/future period. The service checks active organization lineage and non-overlap. For a change against an open current assignment, the service closes the earlier row on the preceding date and creates a new row. Responses identify both the closed and newly created rows where applicable. History remains immutable aside from closing the previously open range.

## Bank accounts

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/employees/:employee_id/bank-accounts` | Own or HR/Owner masked list |
| `POST` | `/employees/:employee_id/bank-accounts` | Add encrypted account (HR/Owner) |
| `PATCH` | `/employees/:employee_id/bank-accounts/:bank_account_id` | Update non-number metadata or replace number (HR/Owner) |
| `POST` | `/employees/:employee_id/bank-accounts/:bank_account_id/make-primary` | Atomic primary switch (HR/Owner) |
| `POST` | `/employees/:employee_id/bank-accounts/:bank_account_id/deactivate` | Deactivate with `replacement_bank_account_id` or `allow_no_primary: true` |

Create/number replacement accepts plaintext `account_number` only on the request boundary. Response includes `account_number_last4` and masked display only. No full number or ciphertext appears in response or audit.

## Weekly holidays

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/employees/:employee_id/weekly-holidays` | Own or HR/Owner history |
| `POST` | `/employees/:employee_id/weekly-holidays` | Add/replacement weekday period (HR/Owner) |
| `POST` | `/employees/:employee_id/weekly-holidays/:holiday_id/end` | End an open rule with `effective_to` (HR/Owner) |

Weekday is integer 0–6. A rule is effective from `effective_from` through `effective_to` inclusive. The same weekday cannot overlap for one employee. Old rows remain readable.

## Stable domain errors

`DUPLICATE_IDENTITY`, `EFFECTIVE_DATE_OVERLAP`, `INVALID_ORGANIZATION_RELATION`, `PRIMARY_BANK_ACCOUNT_CONFLICT`, `RESOURCE_NOT_FOUND`, `FORBIDDEN_SCOPE`, `STATE_CONFLICT`, and `VALIDATION_ERROR` use safe public messages without SQL or protected values.

## Internal downstream service contract

`getEmployeeContextAtDate({ actor, employeeId, date })` returns the authorized employee ID, status, branch/department/position IDs, employment type, base salary, welfare, and effective interval that applied on that business date. It returns no bank number. If no assignment covers the date, it returns an explicit absence result; an out-of-scope employee remains not found. Person B/C call this service interface rather than an A3 repository or controller.
