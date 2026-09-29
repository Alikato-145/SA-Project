# Tasks: System Completion and Release Readiness

**Baseline date**: 2026-09-30

**Branches**: root, `backend/`, and `frontend/` use `develop`

**Purpose**: Close the remaining product, UX, verification, and operational gaps
before Haris Payroll is treated as complete for real users.

## Status and priority

- `[ ]` not completed or not yet proven with repeatable evidence.
- `[X]` completed and verified in the current baseline.
- **P0** blocks the full demo or release decision.
- **P1** is required to satisfy the stated product scope through the web UI.
- **P2** is required before handling real payroll data in production.
- **P3** is intentionally deferred and does not block the current release.

## Confirmed baseline

- [X] T001 Authentication, account lockout, five fixed roles, scoped grants, and
  server-side authorization are implemented.
- [X] T002 Organization, employee, effective-dated employment history, encrypted
  bank accounts, and weekly holidays are implemented.
- [X] T003 Attendance, leave, overtime, advances, loans, debt, payroll,
  payslips, CSV exports, and audit queries are composed in the central backend.
- [X] T004 The frontend exposes the current role-aware dashboard routes and the
  Audit viewer.
- [X] T005 Current automated baseline passes backend typecheck, the PostgreSQL
  integration suite, frontend tests, lint, production build, and Compose config.

## Phase 1 — P0: Prove the complete business journey

**Goal**: One repeatable dataset can demonstrate every role and the complete
employee-to-payslip flow without manual database edits.

- [ ] T006 Create an idempotent release-demo fixture with linked accounts for
  Employee, Supervisor, Branch Manager, HR, and Owner; include two departments,
  two branches, active assignments, payroll configurations, schedules,
  holidays, attendance, leave, OT, finance inputs, and an open payroll period.
- [ ] T007 Add an automated authorization matrix that exercises every released
  route as all five roles and proves both allowed access and safe denial for
  another employee, department, and branch.
- [ ] T008 Run and record the live Employee flow: sign in, inspect own profile,
  submit/edit leave, submit OT, and read only the employee's own payslip.
- [ ] T009 Run and record the live Supervisor flow: inspect only the assigned
  department, manage attendance, approve leave of up to three days, reject a
  four-day approval, and decide OT only within scope.
- [ ] T010 Run and record the live Branch Manager flow: inspect only the assigned
  branch, manage attendance, approve a four-day leave, decide OT, and read only
  payroll records belonging to that branch.
- [ ] T011 Run and record the live HR flow from employee onboarding through
  attendance, approvals, finance, payroll preview, blocker resolution, lock,
  payslip generation, delivery logging, exports, and audit lookup.
- [ ] T012 Run and record the live Owner flow for organization bootstrap,
  account/role administration, last-owner protection, and all-scope oversight.
- [ ] T013 Verify the complete payroll boundary matrix against PostgreSQL:
  incomplete attendance, pending approvals, negative net pay, duplicate record,
  decimal rounding, social-security base, immutable lock, and tracked adjustment.
- [ ] T014 Record commands, fixture identifiers, screenshots, results, known
  limitations, demo date, and approver in `docs/release-checklist.md`.

**Checkpoint**: The system is demo-ready only when T006–T014 are complete.

## Phase 2 — P1: Close missing web functions

**Goal**: Every in-scope backend workflow has a safe, role-appropriate web path.

- [ ] T015 Split the Finance workspace by role. Give Employee a self-only
  advance-request/list view, keep approval plus loan/debt administration for
  HR/Owner, and add frontend and backend regression tests proving that hiding a
  control is never the authorization boundary.
- [ ] T016 Mount a Thai schedule and holiday workspace using the existing
  branch-schedule and holiday-calendar APIs. Replace raw shop/branch IDs with
  named selectors; support effective-dated schedules, date overrides, closing a
  branch for a date, and activating/deactivating public holidays.
- [ ] T017 Show append-only Leave and OT decision history in their workspaces,
  including approver, action, time, remark, and corrected leave type.
- [ ] T018 Complete the Payroll adjustment workspace: list/filter pending and
  historical adjustments, show the original locked record and target period,
  approve/reject with role checks, and show when the adjustment is applied.
- [ ] T019 Implement employee and leave attachment upload/list/download with a
  replaceable storage adapter, MIME/size/hash validation, authorization,
  redacted audit data, and retention of historical metadata. Replace the current
  Documents placeholder and enforce required leave evidence when applicable.
- [ ] T020 Let Employee open a detailed own payslip through the web UI and expose
  a safe printable/downloadable representation. Preserve cross-employee denial
  and voided-payslip behavior.
- [ ] T021 Replace operational raw-ID inputs with named, scoped selectors where
  data already exists: Attendance branch, Finance debt type, Payroll record and
  target period, Payslip/payroll record, and Reports payroll period. Keep IDs as
  secondary reference text.
- [ ] T022 Add a safe temporary-credential lifecycle: require or clearly prompt
  a password change after initial/reset credentials, provide self-service
  password change, revoke existing sessions as defined by policy, and never log
  credentials.
- [ ] T023 Implement scoped management reports for attendance, leave, OT, debt,
  and payroll summaries in addition to the existing bank-transfer and
  social-security CSV exports.

**Checkpoint**: The web UI no longer requires API tools or direct database access
for any in-scope daily workflow.

## Phase 3 — P1: Finish Thai low-tech UX

**Goal**: Users can complete their work without knowing internal IDs or English
domain codes.

- [ ] T024 Complete self-versus-management employee context and regression tests
  from `specs/011-thai-low-tech-ux/tasks.md` T007 and T011.
- [ ] T025 Complete management Leave/OT decision guidance and server-scope
  regression tests from UX tasks T013–T015.
- [ ] T026 Refine Account, Organization, Employee, and Payroll administration
  pages from UX tasks T017–T021, including consequences and recovery paths.
- [ ] T027 Complete public-error and role-visibility coverage from UX task T023.
- [ ] T028 Finish Login and nested HR state/responsive work from UX tasks
  T024 and T026. After login, redirect each role to its first permitted workspace
  or `/dashboard` instead of sending every account to `/payroll`.
- [ ] T029 Apply shared Thai domain/status/date/money labels everywhere from UX
  task T027. Remove remaining English operational labels from released screens.
- [ ] T030 Run the full role and responsive checklist at 360px and 1280px from
  UX task T029; record evidence in `specs/011-thai-low-tech-ux/route-audit.md`.

## Phase 4 — P1: Regression and acceptance coverage

- [ ] T031 Add browser-level tests for login/logout, mobile navigation,
  forbidden recovery, session expiry, and destructive confirmations.
- [ ] T032 Add browser-level tests for Employee leave/OT/payslip and the
  Employee advance path introduced by T015.
- [ ] T033 Add browser-level tests for Supervisor/Branch Manager attendance and
  approval scope, including the three-day/four-day leave boundary.
- [ ] T034 Add browser-level tests for Owner/HR onboarding, account/role
  administration, finance, payroll lock, payslip, export, and Audit workflows.
- [ ] T035 Add contract tests for every list envelope and pagination shape so
  top-level and `meta.pagination` formats cannot drift silently.
- [ ] T036 Make database-gated CI deterministic and process-isolated until the
  shared test-pool lifecycle is redesigned; run Person A, Person B, payroll,
  payslip, report, attachment, and end-to-end suites on disposable PostgreSQL.
- [ ] T037 Add accessibility checks for labels, keyboard flow, focus visibility,
  error announcements, dialogs, tables, and colour-independent status text.

## Phase 5 — P2: Production operations and security

- [ ] T038 Document and test automated PostgreSQL backups, encrypted off-host
  retention, restore verification, recovery-point objective, and recovery-time
  objective in `docs/operations/`.
- [ ] T039 Document the forward migration and rollback/roll-forward procedure;
  rehearse it against a production-like disposable stack.
- [ ] T040 Add structured application logs, request IDs, health/readiness checks,
  failure metrics, and alerting without exposing passwords, tokens, full bank
  accounts, identity numbers, or attachment contents.
- [ ] T041 Define production secret rotation for JWT and bank-encryption key
  versions, including a tested re-encryption procedure and rollback plan.
- [ ] T042 Define audit, payroll, payslip, delivery, and attachment retention;
  verify append-only and locked-record protections through catalog tests.
- [ ] T043 Add rate limiting and abuse monitoring for login and sensitive export
  endpoints in addition to the existing account lockout.
- [ ] T044 Replace or configure the mock mail adapter when real payslip email is
  required; record each attempt and make retries idempotent.
- [ ] T045 Run dependency, container-image, secret-leak, and production-header
  checks; document accepted findings and remediation ownership.
- [ ] T046 Run a clean production deployment rehearsal using only documented
  environment values, verify restart/persistence behavior, and record rollback.

## Phase 6 — Documentation and handoff

- [X] T047 Publish the detailed role-based web guide at
  `docs/user-guide-by-role.md` and clearly mark unavailable functions.
- [ ] T048 Capture final screenshots using non-sensitive demo data and add them
  to the role guide where they materially reduce user error.
- [ ] T049 Update `README.md`, `docs/sprint-readiness.md`,
  `docs/haris-payroll-product-backlog.md`, and `docs/release-checklist.md` so
  their status matches the implemented baseline and this completion plan.
- [ ] T050 Add an operator runbook covering user provisioning, unlock/reset,
  payroll incident handling, failed exports/deliveries, backup restoration, and
  escalation contacts.
- [ ] T051 Obtain sign-off from one representative of each role using the guide;
  record unclear terms, failed steps, and resulting fixes.

## Phase 7 — P3: Explicitly deferred

These items require a separate scope decision and do not block the current
completion plan unless the owner promotes them:

- [ ] T052 External time-clock/device integration with a replaceable adapter.
- [ ] T053 OCR for identity or supporting documents.
- [ ] T054 Multi-factor authentication, forgot-password email, and session-device
  management.
- [ ] T055 Direct bank API submission; the current scope ends at validated CSV.
- [ ] T056 Native mobile applications; the current responsive web application is
  the supported client.

## Dependency order

```text
Demo fixture
  → role matrix and complete journey
  → missing web functions
  → Thai UX and browser regression
  → production operations/security
  → role sign-off and release approval
```

T019 depends on an approved attachment storage and retention policy. T044 depends
on a selected mail provider. T052–T056 must not be started without explicit scope
approval.

## Definition of complete

Haris Payroll is considered complete for release only when:

1. Every P0 and P1 task is checked with repeatable evidence.
2. Each role can finish its documented workflow without direct database access.
3. Authorization is proven server-side for allowed and denied paths.
4. Payroll can be previewed, blocked, locked, adjusted, paid, exported, and
   audited without rewriting historical facts.
5. Backups can be restored and production secrets can be rotated safely.
6. Known P2 exceptions have an owner, risk decision, and target date.
