# Feature Specification: B5 Operations and Payroll Integration

**Feature Branch**: No branch created; specification is independent of implementation branches.

**Created**: 2026-09-28

**Status**: Implemented and validated — 2026-09-29; see validation.md

**Input**: User description: "Complete Person B's B5 integration and fixes: connect existing attendance, schedules, holidays, leave, overtime, advances, loans, and debt workflows to shared sign-in and response conventions; verify their handoff to payroll with Person C."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Use operations through the signed-in application (Priority: P1)

As an authorized manager or HR user, I can record and review attendance through the application using the same sign-in as employee management, so work-day information is available for payroll without manual workarounds.

**Why this priority**: The existing operations features must be reachable and protected before their business rules or payroll handoff can be relied on.

**Independent Test**: Sign in as a branch manager, record a work day for an assigned employee, reload the attendance screen, and confirm the saved record and historical branch. Repeat an attempted action outside the manager's branch and while signed out.

**Acceptance Scenarios**:

1. **Given** an employee has an effective assignment, **When** an authorized manager records attendance for that work date, **Then** the record persists, is visible after reload, and retains the branch effective on that date.
2. **Given** an employee later transfers branches, **When** an authorized user reviews an earlier work day, **Then** its recorded branch remains unchanged.
3. **Given** a manager can manage a branch's schedules and holidays, **When** they save an effective schedule, date override, or holiday through the application, **Then** subsequent attendance for that branch/date uses the applicable values and conflicting effective ranges are rejected.
4. **Given** a signed-out user, expired session, or out-of-scope manager, **When** they attempt to read or change protected operations data, including by addressing a record directly, **Then** access is denied without exposing employee data or changing records.
5. **Given** invalid input, a duplicate work day, or a failed request, **When** the user submits it, **Then** the application explains the reason, preserves entered values where possible, and does not show a successful save.

---

### User Story 2 - Decide leave and overtime safely (Priority: P1)

As an employee, I can submit leave and overtime requests; as an authorized approver, I can decide them and review their history, so payroll receives only valid approved outcomes.

**Why this priority**: Approval failures can cause incorrect deductions, unauthorized payments, or lost quota and decision history.

**Independent Test**: Submit and decide leave and each overtime type for a prepared employee, then inspect quota, attendance, approval history, and payroll preview. Run this journey independently of finance entries.

**Acceptance Scenarios**:

1. **Given** sufficient leave quota and non-overlapping dates, **When** an authorized approver approves leave, **Then** the decision, quota use, and attendance effects succeed together and approved leave does not produce an absence or lateness deduction.
2. **Given** three-day and four-day requests within a supervisor's department, **When** the supervisor decides them, **Then** the three-day request can be approved and the four-day request is denied; an authorized branch manager may approve either directly.
3. **Given** an approver corrects the requested leave type, **When** approval completes, **Then** the original request and corrected decision remain traceable, and quota and attendance reflect the approved type.
4. **Given** rest-day, hourly, and public-holiday overtime requests, **When** authorized decisions are recorded, **Then** all three types retain decision history and only approved overtime becomes payable; a late clock-out alone produces no payable overtime.
5. **Given** overlapping leave, insufficient quota, a repeated decision, or failure during an approval, **When** the operation is attempted, **Then** the request is rejected or rolled back without partial quota use, attendance changes, or duplicate decisions.

---

### User Story 3 - Carry employee finance into payroll (Priority: P1)

As an authorized finance user, I can process advances, loan installments, and food debt, then see the corresponding deductions in payroll, so employees are paid correctly and each deduction is traceable.

**Why this priority**: Finance records must affect payroll accurately without duplicate deductions or loss of financial history.

**Independent Test**: Prepare a complete attendance period, approve an eligible advance, create a due loan installment and debt charge, and compare payroll deductions with their source records before and after locking.

**Acceptance Scenarios**:

1. **Given** the configured standard advance thresholds, **When** eligibility is evaluated at days 19/20, worked-day counts 19/20, and below/at/above half of base salary, **Then** each boundary is enforced and approval is denied if projected net pay would be negative.
2. **Given** an approved advance, a due loan installment, and an unsettled food-debt charge eligible for the period, **When** payroll is previewed, **Then** each appears once with its exact amount and a traceable source; pending or rejected advances are excluded.
3. **Given** a finance user corrects a debt charge, **When** the correction is recorded, **Then** the original transaction remains available and the correction or reversal is separately traceable.
4. **Given** payroll successfully locks, **When** its finance inputs are inspected or another preview is requested, **Then** settlement is recorded consistently and the same source cannot be deducted again in another locked period.
5. **Given** locking fails, **When** finance balances and installment states are inspected, **Then** no partial settlement or installment deduction remains.

---

### User Story 4 - Complete an auditable operations-to-payroll handoff (Priority: P2)

As HR/accounting, I can use approved operational and finance records to preview and lock payroll, identify remaining blockers, and trace the values used, so the integrated sprint demo can be reviewed and repeated.

**Why this priority**: This demonstrates that Person B's work is usable by payroll and provides evidence for Person C's final integration.

**Independent Test**: Use a prepared two-branch scenario to run attendance, leave/overtime approval, finance entry, payroll preview, and lock; separately prepare blocked periods and correction attempts.

**Acceptance Scenarios**:

1. **Given** complete attendance, resolved approvals, valid configuration, and non-negative net pay, **When** HR previews and locks payroll, **Then** the values match the operational sources and the locked record retains a snapshot of all values used.
2. **Given** missing attendance, pending leave/overtime/advance decisions applicable to the period, or negative net pay, **When** locking is attempted, **Then** it is blocked with an actionable reason and no locked record or settlement is partially created.
3. **Given** attendance or approved inputs already used by locked payroll, **When** an ordinary correction would change those historical facts, **Then** the change is rejected and the user is directed to the existing tracked payroll-adjustment workflow.
4. **Given** the complete scenario is repeated on fresh demonstration data, **When** reviewers compare results, **Then** the same inputs produce the same amounts and all protected actions retain their authorization and audit evidence.

### Edge Cases

- An account has no employee association: distinguish the signed-in actor from the employee being managed and do not guess ownership.
- An account has multiple scoped roles: evaluate the permission and its associated scope together; do not combine unrelated permissions and scopes.
- An employee transfers between branches during a period: resolve work-day context for each date and preserve prior branch snapshots.
- A work date falls near midnight: use the project's business-date/time-zone convention consistently across attendance and payroll.
- Large record identifiers and fractional currency amounts: preserve identifiers exactly and money without precision loss across entry, display, and payroll.
- A user submits twice, two approvers act concurrently, or a network failure follows a successful save: reload the actual state and prevent duplicate work days, decisions, settlements, and deductions.
- A protected record is addressed directly or altered input claims another role, branch, or employee: enforce trusted identity and scope independently of supplied values.
- A payroll lock races an attendance correction or approval: preserve a consistent locked snapshot and reject conflicting changes without partial updates.
- A filter returns no results or a session expires during entry: show distinct empty, sign-in-required, forbidden, and failure states without reporting false success.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST make the existing schedule, override, holiday, attendance, leave, overtime, advance, loan/installment, and debt capabilities reachable through the signed-in application and persist successful changes across reloads (Stories 1–3).
- **FR-002**: The system MUST identify the acting account from trusted sign-in state, distinguish it from employee ownership, and reject unauthenticated and expired sessions for every protected operation (Story 1, scenario 4; Edge Cases).
- **FR-003**: The system MUST enforce employee self access, supervisor department scope, branch-manager branch scope, and authorized HR/accounting/owner all-branch duties for both reads and writes, including direct record access (Stories 1–3; Edge Cases).
- **FR-004**: Operations screens MUST follow the application's common sign-in, success, validation, conflict, and failure conventions, preserve exact identifiers and amounts, and display actionable business reasons without revealing internal errors or sensitive account/bank information (Story 1, scenario 5; Edge Cases).
- **FR-005**: Attendance MUST remain unique per employee/work date, retain its historical branch, and use applicable effective schedules, overrides, and holidays; overlapping effective schedules MUST be rejected (Story 1, scenarios 1–3).
- **FR-006**: Leave decisions MUST enforce date overlap and quota rules, the three-day supervisor boundary, and direct branch-manager approval; decision history, corrected leave type, quota, and attendance effects MUST be atomic and traceable (Story 2, scenarios 1–3 and 5).
- **FR-007**: The system MUST retain append-only overtime decisions for all three supported types and make only explicitly approved overtime available for payment (Story 2, scenario 4).
- **FR-008**: Advance approval MUST enforce configured request-date, worked-day, salary-cap, and projected-net-pay eligibility using the same applicable payroll inputs as the preview (Story 3, scenario 1).
- **FR-009**: Loans MUST contribute eligible installments and food debt MUST retain an append-only transaction history, including corrections or reversals, with deductions traceable to their sources (Story 3, scenarios 2–3).
- **FR-010**: Payroll MUST consume the applicable attendance, approved leave/overtime, approved advances, eligible installments, and unsettled debt exactly once, with approved leave distinguished from deductible absence/lateness and exact amounts retained (Stories 2–3; Story 4, scenario 1).
- **FR-011**: Locking MUST enforce complete attendance, resolved applicable approvals, non-negative net pay, and a complete input snapshot; failed or competing changes MUST leave no partial lock, settlement, quota use, or deduction (Stories 2–4; Edge Cases).
- **FR-012**: Ordinary operations edits MUST preserve facts used by locked payroll; post-lock financial corrections MUST use the existing tracked adjustment process (Story 4, scenario 3).
- **FR-013**: Sensitive operational and finance changes MUST retain actor, action, target, old/new values, and time, without passwords, hashes, tokens, or full bank details; approval and debt histories MUST remain inspectable (Stories 2–4).
- **FR-014**: The handoff MUST include repeatable demonstration data, observed results for the complete journey and rejection cases, changes delivered, verification results, and any remaining blockers with an owner (Story 4, scenario 4).

### Key Entities *(include if feature involves data)*

- **Acting account and scoped role**: The signed-in decision-maker, permission type, associated branch/department scope, and optional employee association.
- **Employment context and work day**: An employee's effective assignment and schedule for a date, historical branch, attendance state, time entries, and deduction status.
- **Schedule, override, and holiday**: Effective branch working arrangements and date-specific exceptions that determine attendance expectations.
- **Leave request and decision history**: Requested days/type, approved type, quota effects, approver decisions, and related attendance effects.
- **Overtime request and decision history**: Work date, overtime type, requested/approved quantities, and append-only decisions.
- **Advance, loan installment, and debt transaction**: Eligibility, approval or settlement state, exact amounts, due dates, and traceable financial history.
- **Payroll period, record, snapshot, and adjustment**: The employee-period calculation, consumed source facts, locking blockers, immutable locked values, and tracked corrections.
- **Audit event**: Safe evidence of who changed which record, when, and what changed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every in-scope capability in FR-001 has a recorded passing authorized create-or-decide and read-back scenario in the running application; no scenario needs manual editing of stored records.
- **SC-002**: A prepared scenario covering two branches, a historical transfer, approved leave, all three overtime types, and all three finance categories completes through payroll lock with 100% agreement between expected and displayed amounts, zero duplicate deductions, and zero deductions for approved leave.
- **SC-003**: 100% of defined signed-out, expired-session, cross-employee, cross-department, and cross-branch rejection cases prevent unauthorized reads/writes; allowed cases for all five role types pass.
- **SC-004**: All specified boundary and failure scenarios pass, including leave at three/four days, advance date/worked-day/cap boundaries, duplicate submissions, incomplete attendance, pending approvals, negative net pay, and failed multi-record operations.
- **SC-005**: Every approved leave/overtime decision and finance correction in the demonstration remains traceable, and all attempted ordinary changes to locked-period facts leave the locked values unchanged.
- **SC-006**: A reviewer can repeat the prepared operations-to-payroll journey within 30 minutes using the handoff instructions and obtains the same amounts and outcomes on fresh demonstration data.

## Assumptions

- This is work package B5 from [the two-week plan](../../docs/two-week-three-person-plan.md), completing integration and defects in existing B1–B4 features rather than redesigning those features.
- Existing sign-in, organization/employee history, payroll preview/lock, and tracked adjustment capabilities are dependencies. A defect in a dependency is recorded and coordinated with its owner when it blocks this scope.
- Person B owns operational and finance feature changes. Person C coordinates shared application composition, navigation, response conventions, and payroll changes; work on the same shared files is sequenced during planning.
- The current project guide and constitution define business rules. Configured advance thresholds are used; date 20, 20 worked days, and half of base salary are the standard boundary examples.
- The existing data model and migrations remain frozen. A mismatch is reported to the schema owner instead of being resolved by changing historical records or silently weakening requirements.
- New payroll algorithms, payslip/export features, visual redesign, external time clocks, OCR, real email, and cloud attachments are outside B5. Schedule/holiday controls necessary to exercise existing B1 workflows are within scope.
- Demonstration and destructive failure verification use disposable data. Existing payroll, employment, approval, and debt histories are preserved.
- This invocation produces the specification and requirements-quality checklist. Technical design, executable tasks, implementation, and runtime verification follow in later phases.
