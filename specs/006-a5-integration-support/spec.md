# Feature Specification: A5 Integration Support

**Branch**: codex/a5-integration-support | **Date**: 2026-09-29 | **Status**: In progress

## User Stories

### US1 — Historical employee context (P1)

Attendance and payroll use branch, department, salary, and welfare effective on each work date, not the current assignment.

**Independent test**: A transfer/pay change resolves correctly before and on its effective date.

1. Given a transfer, attendance scope and branch use the respective historical assignment.
2. Given a mid-period pay change, daily earnings use the effective compensation and exact decimals.
3. Given no assignment, context fails closed with a stable missing-assignment error.

### US2 — Role and audit integration (P1)

The five Person A roles are authorized by dated scope; registered A1–A3 actions are audited with secrets redacted.

**Independent test**: Five-role matrix and audit registry/redaction suite run without a database.

1. Employee self access never grants another employee's data or management actions.
2. Supervisor and branch manager access follows the historical department/branch.
3. HR and owner all-scope grants span every branch.
4. Sensitive actions have audit coverage without passwords, hashes, tokens, or full bank account numbers.

### US3 — Reproducible demo handoff (P2)

The team can rehearse login → employee → history with exact check results or named blockers.

**Independent test**: Commands, actual outcomes, and environment gaps are recorded.

## Requirements

- FR-001: Verify dated employee context at transfer/pay boundaries for attendance and payroll.
- FR-002: Verify backend self/department/branch/all authorization, including owner all-branch access.
- FR-003: Verify A1–A3 audit action coverage and redaction.
- FR-004: Fix only confirmed integration defects; no schema/migration or unrelated feature changes.
- FR-005: Record reproducible checks and truthful demo limitations.

## Edge Cases

- New effective row applies on its start date; the previous row does not.
- Grants from different scopes must not combine to elevate authority.
- Missing assignment must not fall back to today's row.
- Audit serialization redacts secrets and full bank numbers.

## Success Criteria

- SC-001: Five-role matrix covers self, department, branch, global, and transfer dates.
- SC-002: Attendance/payroll checks pass on both sides of effective-date changes.
