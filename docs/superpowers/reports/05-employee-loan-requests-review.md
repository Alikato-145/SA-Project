# Subtask 5 — Independent review

## Spec compliance: PASS

Reviewed the frozen task-1 review package and actual loan-request service, runtime, repository, routes, controller, mapper, schema/migration, shared transaction/runtime and employee authorization implementation; compared the brief, plan Global Constraints/Review Focus, implementation report, frontend Finance page, E2E cases and logical references. Applied the clarified policy that request approval cannot start before the current Bangkok month; existing direct HR loan behavior remains unchanged.

No actionable product findings found. Own employee identity is checked server-side before list/create, while finance decisions require an active all-scope HR/OWNER grant. Requested terms and server-owned fields cannot be changed by the public API. Approval acquires common payroll serialization before request row locking, joins the existing transaction through AsyncLocalStorage, creates the loan through the existing service, checks the entire installment interval and persists the decision atomically. Repeated or concurrent decisions cannot create a second loan. Rejection requires a nonblank note. Controller/mapper boundaries and feature ownership are preserved. The new UI provides request entry, persisted decision history, finance controls and the existing approved-loan installment display.

The additive migration and feature schema agree on the enum, 4 restrictive foreign keys, unique nullable loan link, employee/status index and decision checks. DBML/reference additions describe the same model.

## Task quality: PASS

The focused real-DB tests exercise real transaction rollback after an installment constraint error, duplicate/concurrent decisions, full-schedule lock denial and approval waiting behind the payroll advisory lock. Browser cases cover employee submission/reload, HR approval, OWNER rejection and denied forged/manager decisions. These are meaningful checks of the requested behavior rather than assertions inferred solely from the implementation.

The frozen package initially retained a 37-primary-key catalog expectation. Inspected the final test-only delta in `catalog-fix-diff.md` and actual `backend/src/core/db/database.integration.test.ts`: the expected count is now 38 and the assertion that every primary key is bigint remains intact. Catalog expectations now consistently require 38 tables, 23 enums and 4 migrations. Inspected root's final log `/private/tmp/haris-task5-final-db.log`: 514 passed, 0 skipped, 0 failed across 109 files. Root also reports typecheck passing. The verification-only defect is closed; no actionable findings remain.

Review was read-only apart from this report. No tests, database operations, browser operations or source edits were performed by this reviewer. Verification execution remains owned by root; supplied passing results and the inspected final log were considered evidence, not a substitute for inspecting the implementation.
