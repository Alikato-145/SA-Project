# B1 Data Model

The following frozen entities are owned by Person B for behavior implementation.
Their Drizzle schemas and migration must not change.

## Branch schedule

| Field | Meaning | Rule |
|---|---|---|
| `branch_id` | Branch receiving the schedule | Must be within actor scope. |
| `work_start_time` | Normal shift start | Required. |
| `standard_close_time` | Normal shift close | Required; later than start. |
| `late_grace_minutes` | Late-arrival grace | Non-negative. |
| `effective_from` / `effective_to` | Inclusive schedule range | End is on/after start; no overlap for the branch. |

Ranges sharing an end/start date overlap.

## Schedule override

| Field | Meaning | Rule |
|---|---|---|
| `branch_id`, `schedule_date` | One exception for one branch/date | Unique pair. |
| `is_closed` | Branch has no working shift | Requires no working hours. |
| `work_start_time`, `close_time` | Replacement hours | Both required when open; close follows start. |
| `reason` | Explanation | Optional. |

## Holiday calendar

| Field | Meaning | Rule |
|---|---|---|
| `shop_id`, `holiday_date` | Shop-wide public holiday | Unique pair. |
| `name` | Display name | Required. |
| `is_active` | Whether attendance considers it | Inactive entries are excluded. |

## Work-day record

| Field | Meaning | Rule |
|---|---|---|
| `employee_id`, `work_date` | Attendance for one date | Unique pair. |
| `branch_id` | Branch actually worked | Immutable snapshot after creation. |
| `status` | Attendance outcome | Frozen `work_day_status` enum value. |
| `clock_in_at`, `clock_out_at` | Actual UTC work instants | End is not earlier than start. |
| `late_minutes` | Recorded lateness | Non-negative. |
| `is_deductible` | Payroll deduction signal | Explicit Boolean. |
| `entry_source` | Entry source | B1 writes `manual`. |
| `created_by_user_account_id` | Recording actor | Read from authenticated context. |

## Relationships and consumers

Leave and overtime can reference a work-day record. Payroll reads records by
employee/date range and uses the stored status, branch, clock values, lateness,
deduction flag and source without resolving a later assignment.
