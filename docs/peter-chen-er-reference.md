# Haris Payroll — Peter Chen ER reference

Read-only schema reference, inspected 14 October 2026. Sources: canonical DBML and feature-owned Drizzle schema. No schema/migration was changed.

## Inventory: 36 entities / 79 declared FK relationships

Every entity has `id` as its primary key. Underline this attribute in Chen notation. FK columns below describe the relational implementation; in a conceptual Chen diagram, draw a named diamond instead of repeating its FK as an oval.

For each relationship A → B below: the A-side range is how many A rows one B row may reference; the B-side range is how many B rows one A row may have. A nullable FK means partial participation on B; a required FK means total participation on B. Parent rows generally allow zero children.

## Entities and attributes

### shops

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `code` | `varchar(30)` | UNIQUE | Yes |
| `name` | `varchar(150)` | — | Yes |
| `is_active` | `boolean` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### branches

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `shop_id` | `bigint` | FK → shops.id | Yes |
| `code` | `varchar(30)` | — | Yes |
| `name` | `varchar(150)` | — | Yes |
| `address` | `text` | — | No |
| `timezone` | `varchar(50)` | — | Yes |
| `is_active` | `boolean` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(shop_id, code)`.

### departments

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `branch_id` | `bigint` | FK → branches.id | Yes |
| `code` | `varchar(30)` | — | Yes |
| `name` | `varchar(100)` | — | Yes |
| `is_active` | `boolean` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(branch_id, code)`.

### positions

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `shop_id` | `bigint` | FK → shops.id | Yes |
| `code` | `varchar(30)` | — | Yes |
| `name` | `varchar(100)` | — | Yes |
| `is_active` | `boolean` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(shop_id, code)`.

### employees

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_code` | `varchar(30)` | UNIQUE | Yes |
| `national_id` | `varchar(20)` | UNIQUE | No |
| `passport_id` | `varchar(30)` | UNIQUE | No |
| `first_name` | `varchar(100)` | — | Yes |
| `last_name` | `varchar(100)` | — | Yes |
| `phone` | `varchar(30)` | — | No |
| `personal_email` | `varchar(255)` | — | No |
| `address` | `text` | — | No |
| `hire_date` | `date` | — | Yes |
| `status` | `employee_status` | — | Yes |
| `terminated_at` | `date` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(20)`; `(30)`.

### user_accounts

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | UNIQUE; FK → employees.id | No |
| `username` | `varchar(100)` | UNIQUE | Yes |
| `password_hash` | `text` | — | Yes |
| `status` | `account_status` | — | Yes |
| `failed_login_attempts` | `smallint` | — | Yes |
| `locked_until` | `timestamptz` | — | No |
| `last_login_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### roles

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `code` | `varchar(30)` | UNIQUE | Yes |
| `name` | `varchar(100)` | — | Yes |
| `scope` | `role_scope` | — | Yes |
| `is_active` | `boolean` | — | Yes |

### user_account_roles

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `role_id` | `bigint` | FK → roles.id | Yes |
| `branch_id` | `bigint` | FK → branches.id | No |
| `department_id` | `bigint` | FK → departments.id | No |
| `granted_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `granted_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(user_account_id, role_id, branch_id, department_id)`.

### employment_assignments

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `branch_id` | `bigint` | FK → branches.id | Yes |
| `department_id` | `bigint` | FK → departments.id | Yes |
| `position_id` | `bigint` | FK → positions.id | Yes |
| `employment_type` | `employment_type` | — | Yes |
| `base_salary` | `numeric(12,2)` | — | Yes |
| `welfare_amount` | `numeric(12,2)` | — | Yes |
| `effective_from` | `date` | — | Yes |
| `effective_to` | `date` | — | No |
| `is_primary` | `boolean` | — | Yes |
| `created_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### employee_bank_accounts

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `bank_code` | `varchar(20)` | — | Yes |
| `bank_name` | `varchar(100)` | — | Yes |
| `account_holder_name` | `varchar(200)` | — | Yes |
| `account_number_ciphertext` | `text` | — | Yes |
| `account_number_last4` | `varchar(4)` | — | Yes |
| `is_primary` | `boolean` | — | Yes |
| `is_active` | `boolean` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### employee_weekly_holidays

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `weekday` | `smallint` | — | Yes |
| `effective_from` | `date` | — | Yes |
| `effective_to` | `date` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### branch_schedules

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `branch_id` | `bigint` | FK → branches.id | Yes |
| `work_start_time` | `time` | — | Yes |
| `standard_close_time` | `time` | — | Yes |
| `late_grace_minutes` | `smallint` | — | Yes |
| `effective_from` | `date` | — | Yes |
| `effective_to` | `date` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### branch_schedule_overrides

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `branch_id` | `bigint` | FK → branches.id | Yes |
| `schedule_date` | `date` | — | Yes |
| `work_start_time` | `time` | — | No |
| `close_time` | `time` | — | No |
| `is_closed` | `boolean` | — | Yes |
| `reason` | `varchar(255)` | — | No |
| `created_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(branch_id, schedule_date)`.

### holiday_calendars

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `shop_id` | `bigint` | FK → shops.id | Yes |
| `holiday_date` | `date` | — | Yes |
| `name` | `varchar(150)` | — | Yes |
| `is_active` | `boolean` | — | Yes |
| `created_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(shop_id, holiday_date)`.

### work_day_records

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `branch_id` | `bigint` | FK → branches.id | Yes |
| `work_date` | `date` | — | Yes |
| `clock_in_at` | `timestamptz` | — | No |
| `clock_out_at` | `timestamptz` | — | No |
| `status` | `work_day_status` | — | Yes |
| `late_minutes` | `integer` | — | Yes |
| `is_deductible` | `boolean` | — | Yes |
| `entry_source` | `time_entry_source` | — | Yes |
| `created_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `note` | `text` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(employee_id, work_date)`.

### leave_types

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `code` | `varchar(30)` | UNIQUE | Yes |
| `name_th` | `varchar(100)` | — | Yes |
| `quota_type` | `quota_type` | — | Yes |
| `quota_days` | `numeric(8,2)` | — | No |
| `is_deductible` | `boolean` | — | Yes |
| `requires_document` | `boolean` | — | Yes |
| `allow_exceed` | `boolean` | — | Yes |
| `is_active` | `boolean` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### leave_requests

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `original_leave_type_id` | `bigint` | FK → leave_types.id | Yes |
| `final_leave_type_id` | `bigint` | FK → leave_types.id | No |
| `start_date` | `date` | — | Yes |
| `end_date` | `date` | — | Yes |
| `requested_days` | `numeric(8,2)` | — | Yes |
| `reason` | `text` | — | No |
| `status` | `leave_request_status` | — | Yes |
| `is_retroactive` | `boolean` | — | Yes |
| `submitted_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `submitted_at` | `timestamptz` | — | Yes |
| `decided_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### leave_request_days

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `leave_request_id` | `bigint` | FK → leave_requests.id | Yes |
| `work_day_record_id` | `bigint` | UNIQUE; FK → work_day_records.id | No |
| `leave_type_id` | `bigint` | FK → leave_types.id | Yes |
| `leave_date` | `date` | — | Yes |
| `day_amount` | `numeric(8,2)` | — | Yes |
| `is_paid` | `boolean` | — | Yes |
| `is_deductible` | `boolean` | — | Yes |
| `quota_consumed` | `numeric(8,2)` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(leave_request_id, leave_date)`.

### leave_quotas

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `leave_type_id` | `bigint` | FK → leave_types.id | Yes |
| `quota_year` | `smallint` | — | Yes |
| `entitled_days` | `numeric(8,2)` | — | Yes |
| `used_days` | `numeric(8,2)` | — | Yes |
| `last_recalculated_at` | `timestamptz` | — | No |
| `frozen_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(employee_id, leave_type_id, quota_year)`.

### leave_approval_actions

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `leave_request_id` | `bigint` | FK → leave_requests.id | Yes |
| `actor_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `action` | `approval_action_type` | — | Yes |
| `from_leave_type_id` | `bigint` | FK → leave_types.id | No |
| `to_leave_type_id` | `bigint` | FK → leave_types.id | No |
| `remark` | `text` | — | No |
| `acted_at` | `timestamptz` | — | Yes |

### overtime_records

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `work_day_record_id` | `bigint` | FK → work_day_records.id | No |
| `overtime_date` | `date` | — | Yes |
| `overtime_type` | `overtime_type` | — | Yes |
| `hours` | `numeric(8,2)` | — | No |
| `day_units` | `numeric(8,2)` | — | No |
| `reason` | `text` | — | No |
| `status` | `overtime_status` | — | Yes |
| `requested_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `submitted_at` | `timestamptz` | — | Yes |
| `decided_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(employee_id, overtime_date)`.

### overtime_approval_actions

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `overtime_record_id` | `bigint` | FK → overtime_records.id | Yes |
| `actor_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `action` | `approval_action_type` | — | Yes |
| `remark` | `text` | — | No |
| `acted_at` | `timestamptz` | — | Yes |

### advance_requests

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `request_month` | `date` | — | Yes |
| `amount` | `numeric(12,2)` | — | Yes |
| `status` | `advance_status` | — | Yes |
| `requested_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `requested_at` | `timestamptz` | — | Yes |
| `decided_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `decided_at` | `timestamptz` | — | No |
| `decision_note` | `text` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### loans

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `principal_amount` | `numeric(12,2)` | — | Yes |
| `reason` | `text` | — | Yes |
| `installment_count` | `smallint` | — | Yes |
| `status` | `loan_status` | — | Yes |
| `approved_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `approved_at` | `timestamptz` | — | Yes |
| `closed_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### loan_installments

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `loan_id` | `bigint` | FK → loans.id | Yes |
| `installment_no` | `smallint` | — | Yes |
| `due_period_start` | `date` | — | Yes |
| `amount` | `numeric(12,2)` | — | Yes |
| `status` | `installment_status` | — | Yes |
| `deducted_at` | `timestamptz` | — | No |
| `payroll_record_id` | `bigint` | FK → payroll_records.id | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(loan_id, installment_no)`.

### debt_types

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `code` | `varchar(30)` | UNIQUE | Yes |
| `name_th` | `varchar(100)` | — | Yes |
| `description` | `text` | — | No |
| `is_active` | `boolean` | — | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### debt_transactions

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `debt_type_id` | `bigint` | FK → debt_types.id | Yes |
| `transaction_kind` | `debt_transaction_kind` | — | Yes |
| `transaction_date` | `date` | — | Yes |
| `description` | `text` | — | Yes |
| `amount` | `numeric(12,2)` | — | Yes |
| `original_transaction_id` | `bigint` | FK → debt_transactions.id | No |
| `recorded_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `settled_in_payroll_record_id` | `bigint` | FK → payroll_records.id | No |
| `settled_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### payroll_configurations

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `shop_id` | `bigint` | FK → shops.id | Yes |
| `branch_id` | `bigint` | FK → branches.id | No |
| `config_key` | `varchar(50)` | — | Yes |
| `numeric_value` | `numeric(14,4)` | — | Yes |
| `unit` | `varchar(30)` | — | Yes |
| `effective_from` | `date` | — | Yes |
| `effective_to` | `date` | — | No |
| `created_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

### payroll_periods

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `shop_id` | `bigint` | FK → shops.id | Yes |
| `period_year` | `smallint` | — | Yes |
| `period_month` | `smallint` | — | Yes |
| `start_date` | `date` | — | Yes |
| `end_date` | `date` | — | Yes |
| `status` | `payroll_period_status` | — | Yes |
| `created_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `previewed_at` | `timestamptz` | — | No |
| `locked_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `locked_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(shop_id, period_year, period_month)`.

### payroll_records

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `payroll_period_id` | `bigint` | FK → payroll_periods.id | Yes |
| `employee_id` | `bigint` | FK → employees.id | Yes |
| `employment_assignment_id` | `bigint` | FK → employment_assignments.id | Yes |
| `status` | `payroll_record_status` | — | Yes |
| `base_salary_snapshot` | `numeric(12,2)` | — | Yes |
| `welfare_snapshot` | `numeric(12,2)` | — | Yes |
| `total_earnings` | `numeric(12,2)` | — | Yes |
| `total_deductions` | `numeric(12,2)` | — | Yes |
| `net_pay` | `numeric(12,2)` | — | Yes |
| `calculated_at` | `timestamptz` | — | No |
| `calculated_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `locked_at` | `timestamptz` | — | No |
| `created_at` | `timestamptz` | — | Yes |
| `updated_at` | `timestamptz` | — | Yes |

DBML composite UNIQUE: `(payroll_period_id, employee_id)`.

### payroll_items

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `payroll_record_id` | `bigint` | FK → payroll_records.id | Yes |
| `item_type` | `payroll_item_type` | — | Yes |
| `direction` | `payroll_item_direction` | — | Yes |
| `description` | `varchar(255)` | — | Yes |
| `quantity` | `numeric(10,2)` | — | No |
| `rate` | `numeric(14,4)` | — | No |
| `amount` | `numeric(12,2)` | — | Yes |
| `payroll_configuration_id` | `bigint` | FK → payroll_configurations.id | No |
| `source_table` | `varchar(80)` | — | No |
| `source_id` | `bigint` | — | No |
| `occurred_on` | `date` | — | No |
| `created_at` | `timestamptz` | — | Yes |

### payroll_adjustments

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `original_payroll_record_id` | `bigint` | FK → payroll_records.id | Yes |
| `applied_payroll_period_id` | `bigint` | FK → payroll_periods.id | No |
| `direction` | `payroll_item_direction` | — | Yes |
| `amount` | `numeric(12,2)` | — | Yes |
| `reason` | `text` | — | Yes |
| `status` | `payroll_adjustment_status` | — | Yes |
| `requested_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `requested_at` | `timestamptz` | — | Yes |
| `approved_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `approved_at` | `timestamptz` | — | No |
| `applied_payroll_item_id` | `bigint` | UNIQUE; FK → payroll_items.id | No |

### payslips

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `payroll_record_id` | `bigint` | UNIQUE; FK → payroll_records.id | Yes |
| `file_storage_key` | `text` | — | Yes |
| `file_sha256` | `varchar(64)` | — | Yes |
| `status` | `payslip_status` | — | Yes |
| `generated_at` | `timestamptz` | — | Yes |
| `generated_by_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `voided_at` | `timestamptz` | — | No |
| `voided_by_user_account_id` | `bigint` | FK → user_accounts.id | No |

### email_delivery_logs

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `payslip_id` | `bigint` | FK → payslips.id | Yes |
| `recipient_email` | `varchar(255)` | — | Yes |
| `status` | `email_delivery_status` | — | Yes |
| `provider_message_id` | `varchar(255)` | — | No |
| `attempted_at` | `timestamptz` | — | Yes |
| `sent_at` | `timestamptz` | — | No |
| `error_message` | `text` | — | No |

### attachments

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `employee_id` | `bigint` | FK → employees.id | No |
| `leave_request_id` | `bigint` | FK → leave_requests.id | No |
| `file_name` | `varchar(255)` | — | Yes |
| `storage_key` | `text` | — | Yes |
| `mime_type` | `varchar(100)` | — | Yes |
| `file_size_bytes` | `bigint` | — | Yes |
| `file_sha256` | `varchar(64)` | — | Yes |
| `uploaded_by_user_account_id` | `bigint` | FK → user_accounts.id | Yes |
| `uploaded_at` | `timestamptz` | — | Yes |

### audit_logs

| Attribute | DBML type | Key / reference | Required in Drizzle |
|---|---|---|---|
| `id` | `bigint` | PK | Yes |
| `actor_user_account_id` | `bigint` | FK → user_accounts.id | No |
| `action` | `varchar(80)` | — | Yes |
| `table_name` | `varchar(100)` | — | Yes |
| `record_id` | `varchar(100)` | — | Yes |
| `old_data` | `jsonb` | — | No |
| `new_data` | `jsonb` | — | No |
| `reason` | `text` | — | No |
| `occurred_at` | `timestamptz` | — | Yes |
| `request_id` | `varchar(100)` | — | No |

## Complete relationship list

| A: referenced entity | Relationship / B foreign key | B: referencing entity | A-side range | B-side range |
|---|---|---|---|---|
| `shops` | `shop_id` | `branches` | 1 | 0..N |
| `branches` | `branch_id` | `departments` | 1 | 0..N |
| `shops` | `shop_id` | `positions` | 1 | 0..N |
| `employees` | `employee_id` | `user_accounts` | 0..1 | 0..1 |
| `user_accounts` | `user_account_id` | `user_account_roles` | 1 | 0..N |
| `roles` | `role_id` | `user_account_roles` | 1 | 0..N |
| `branches` | `branch_id` | `user_account_roles` | 0..1 | 0..N |
| `departments` | `department_id` | `user_account_roles` | 0..1 | 0..N |
| `user_accounts` | `granted_by_user_account_id` | `user_account_roles` | 0..1 | 0..N |
| `employees` | `employee_id` | `employment_assignments` | 1 | 0..N |
| `branches` | `branch_id` | `employment_assignments` | 1 | 0..N |
| `departments` | `department_id` | `employment_assignments` | 1 | 0..N |
| `positions` | `position_id` | `employment_assignments` | 1 | 0..N |
| `user_accounts` | `created_by_user_account_id` | `employment_assignments` | 0..1 | 0..N |
| `employees` | `employee_id` | `employee_bank_accounts` | 1 | 0..N |
| `employees` | `employee_id` | `employee_weekly_holidays` | 1 | 0..N |
| `branches` | `branch_id` | `branch_schedules` | 1 | 0..N |
| `branches` | `branch_id` | `branch_schedule_overrides` | 1 | 0..N |
| `user_accounts` | `created_by_user_account_id` | `branch_schedule_overrides` | 0..1 | 0..N |
| `shops` | `shop_id` | `holiday_calendars` | 1 | 0..N |
| `user_accounts` | `created_by_user_account_id` | `holiday_calendars` | 0..1 | 0..N |
| `employees` | `employee_id` | `work_day_records` | 1 | 0..N |
| `branches` | `branch_id` | `work_day_records` | 1 | 0..N |
| `user_accounts` | `created_by_user_account_id` | `work_day_records` | 0..1 | 0..N |
| `employees` | `employee_id` | `leave_requests` | 1 | 0..N |
| `leave_types` | `original_leave_type_id` | `leave_requests` | 1 | 0..N |
| `leave_types` | `final_leave_type_id` | `leave_requests` | 0..1 | 0..N |
| `user_accounts` | `submitted_by_user_account_id` | `leave_requests` | 1 | 0..N |
| `leave_requests` | `leave_request_id` | `leave_request_days` | 1 | 0..N |
| `work_day_records` | `work_day_record_id` | `leave_request_days` | 0..1 | 0..1 |
| `leave_types` | `leave_type_id` | `leave_request_days` | 1 | 0..N |
| `employees` | `employee_id` | `leave_quotas` | 1 | 0..N |
| `leave_types` | `leave_type_id` | `leave_quotas` | 1 | 0..N |
| `leave_requests` | `leave_request_id` | `leave_approval_actions` | 1 | 0..N |
| `user_accounts` | `actor_user_account_id` | `leave_approval_actions` | 1 | 0..N |
| `leave_types` | `from_leave_type_id` | `leave_approval_actions` | 0..1 | 0..N |
| `leave_types` | `to_leave_type_id` | `leave_approval_actions` | 0..1 | 0..N |
| `employees` | `employee_id` | `overtime_records` | 1 | 0..N |
| `work_day_records` | `work_day_record_id` | `overtime_records` | 0..1 | 0..N |
| `user_accounts` | `requested_by_user_account_id` | `overtime_records` | 1 | 0..N |
| `overtime_records` | `overtime_record_id` | `overtime_approval_actions` | 1 | 0..N |
| `user_accounts` | `actor_user_account_id` | `overtime_approval_actions` | 1 | 0..N |
| `employees` | `employee_id` | `advance_requests` | 1 | 0..N |
| `user_accounts` | `requested_by_user_account_id` | `advance_requests` | 1 | 0..N |
| `user_accounts` | `decided_by_user_account_id` | `advance_requests` | 0..1 | 0..N |
| `employees` | `employee_id` | `loans` | 1 | 0..N |
| `user_accounts` | `approved_by_user_account_id` | `loans` | 1 | 0..N |
| `loans` | `loan_id` | `loan_installments` | 1 | 0..N |
| `payroll_records` | `payroll_record_id` | `loan_installments` | 0..1 | 0..N |
| `employees` | `employee_id` | `debt_transactions` | 1 | 0..N |
| `debt_types` | `debt_type_id` | `debt_transactions` | 1 | 0..N |
| `debt_transactions` | `original_transaction_id` | `debt_transactions` | 0..1 | 0..N |
| `user_accounts` | `recorded_by_user_account_id` | `debt_transactions` | 1 | 0..N |
| `payroll_records` | `settled_in_payroll_record_id` | `debt_transactions` | 0..1 | 0..N |
| `shops` | `shop_id` | `payroll_configurations` | 1 | 0..N |
| `branches` | `branch_id` | `payroll_configurations` | 0..1 | 0..N |
| `user_accounts` | `created_by_user_account_id` | `payroll_configurations` | 1 | 0..N |
| `shops` | `shop_id` | `payroll_periods` | 1 | 0..N |
| `user_accounts` | `created_by_user_account_id` | `payroll_periods` | 1 | 0..N |
| `user_accounts` | `locked_by_user_account_id` | `payroll_periods` | 0..1 | 0..N |
| `payroll_periods` | `payroll_period_id` | `payroll_records` | 1 | 0..N |
| `employees` | `employee_id` | `payroll_records` | 1 | 0..N |
| `employment_assignments` | `employment_assignment_id` | `payroll_records` | 1 | 0..N |
| `user_accounts` | `calculated_by_user_account_id` | `payroll_records` | 0..1 | 0..N |
| `payroll_records` | `payroll_record_id` | `payroll_items` | 1 | 0..N |
| `payroll_configurations` | `payroll_configuration_id` | `payroll_items` | 0..1 | 0..N |
| `payroll_records` | `original_payroll_record_id` | `payroll_adjustments` | 1 | 0..N |
| `payroll_periods` | `applied_payroll_period_id` | `payroll_adjustments` | 0..1 | 0..N |
| `user_accounts` | `requested_by_user_account_id` | `payroll_adjustments` | 1 | 0..N |
| `user_accounts` | `approved_by_user_account_id` | `payroll_adjustments` | 0..1 | 0..N |
| `payroll_items` | `applied_payroll_item_id` | `payroll_adjustments` | 0..1 | 0..1 |
| `payroll_records` | `payroll_record_id` | `payslips` | 1 | 0..1 |
| `user_accounts` | `generated_by_user_account_id` | `payslips` | 0..1 | 0..N |
| `user_accounts` | `voided_by_user_account_id` | `payslips` | 0..1 | 0..N |
| `payslips` | `payslip_id` | `email_delivery_logs` | 1 | 0..N |
| `employees` | `employee_id` | `attachments` | 0..1 | 0..N |
| `leave_requests` | `leave_request_id` | `attachments` | 0..1 | 0..N |
| `user_accounts` | `uploaded_by_user_account_id` | `attachments` | 1 | 0..N |
| `user_accounts` | `actor_user_account_id` | `audit_logs` | 0..1 | 0..N |

## Chen modelling decisions and constraints

- `user_accounts` ↔ `roles` is M:N via the associative entity `user_account_roles`. Keep it as an entity when showing scoped grants, grantor and grant time.
- `employees` ↔ `leave_types` is M:N over yearly quotas via `leave_quotas`; year is part of the uniqueness constraint.
- `employees` ↔ `payroll_periods` is M:N via `payroll_records`, unique per employee and period.
- `employment_assignments` is a dated entity joining employee, branch, department and position, with salary/welfare attributes. Do not draw a direct employee→current branch relation that discards history.
- `employees` ↔ `user_accounts`: optional one-to-one on both sides. An employee may have no login; an administrative account may have no employee.
- `payroll_records` → `payslips`: one record has 0..1 slip; each slip requires exactly one record.
- `work_day_records` ↔ `leave_request_days`: optional one-to-one in Drizzle because `work_day_record_id` is UNIQUE. DBML omits this uniqueness.
- `payroll_items` ↔ `payroll_adjustments`: optional one-to-one via UNIQUE `applied_payroll_item_id` in Drizzle. DBML omits this uniqueness.
- `payroll_adjustments.applied_payroll_period_id` is nullable in Drizzle (DBML currently marks it required). Pending adjustments may not have a destination period.
- `attachments` belongs to exactly one employee OR leave request (XOR). Each separate ownership FK is nullable, but both cannot be empty or populated together.
- `debt_transactions.original_transaction_id` is a recursive optional relation; distinguish original transaction and reversing/adjusting transaction roles.
- Account action relationships (creator, requester, approver, grantor, locker, uploader, actor) must be separately named when multiple lines connect the same two entities.
- `payroll_items.source_table/source_id` and `audit_logs.table_name/record_id` are generic application references, not declared foreign keys. Do not draw them as enforced FK relationships.
- Work-day branch and payroll salary/welfare are historical snapshots; keep them as stored attributes rather than derived attributes.
- `effective_from/effective_to` ranges for assignments, weekly holidays, schedules and configurations must not overlap within their defined scope.
- A work-day is unique per employee/date; payroll record per employee/period; OT record per employee/date; installment per loan/installment number.
- All entities have their own surrogate ID. Having a required parent FK alone does not make an entity weak in Chen notation; only use weak-entity notation for an explicitly remodelled conceptual entity identified by parent key plus partial key.
- Enums are attribute domains, not separate entity tables. Bank names/codes, work statuses and OT types are not master entities in this schema.

## DBML / executable-schema differences

The attribute type column reproduces DBML. Required/optional and the FK cardinality table follow inspected Drizzle column definitions. Besides the three relationship differences noted above, Drizzle uses nullable OT hours/day_units with a mutually exclusive type check, rather than both required zero-default columns as in DBML. Use executable schema for an implementation ERD and record these mismatches for the schema owner; do not silently edit either source.
