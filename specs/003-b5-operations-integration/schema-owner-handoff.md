# Schema Owner Handoff: Debt Settlement Fields

Discovered 2026-09-29 during B5 database-backed validation.

The frozen migration installs `debt_transactions_append_only`, rejecting every UPDATE/DELETE. Existing payroll settlement attempted to update `settled_at`, `settled_in_payroll_record_id`, and `updated_at`, so a real payroll lock failed even though mocked tests passed.

No schema or migration has been changed. B5 preserves original debt rows and records settlement through existing immutable locked payroll items (`source_table=debt_transactions`, `source_id=<original transaction>`). Candidate projection excludes sources already linked to locked records; debt ledger reads derive settlement record/time from that evidence; reversal is denied after such consumption. Final record locking, loan/advance state changes and audit evidence commit atomically.

Please review whether the logical references should describe derived settlement, or a separately coordinated future schema change should explicitly permit settlement-only metadata updates. Historical transaction content and immutable payroll protections must remain unchanged either way. This is a schema-owner follow-up, not a B5 migration task.
