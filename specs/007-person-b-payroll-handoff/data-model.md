# B5 Data Model

No schema changes. Existing `work_day_records` is unique per employee/date and stores a historical `branch_id`. Existing approved leave days carry final `is_deductible` and leave date. The attendance effect writes only a work-day status/deduction or inserts a new leave work day with the effective branch snapshot. Present/late/holiday records are not overwritten.
