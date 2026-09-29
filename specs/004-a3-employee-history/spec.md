# Feature Specification: A3 Employee Master and History

**Feature Branch**: `004-a3-employee-history`

**Created**: 2026-09-23

**Status**: Draft

**Input**: Continue Person A after A1/A2, following `docs/person-a-detailed-work-plan.md` A3 and the approved employee data model.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Find and inspect employees within scope (Priority: P1)

HR and Owner browse the complete employee register. A branch manager sees only employees assigned to the granted branch; a supervisor sees only employees assigned to the granted department; an employee sees only their own profile. Team readers receive basic work identity and contact context, while compensation, full identity numbers, and bank information remain private.

**Why this priority**: Every later employment and payroll action starts from a correctly identified employee and effective organization context.

**Independent Test**: Create employees assigned to two branches and two departments, query as all five roles, and verify both visible records and withheld fields.

**Acceptance Scenarios**:

1. **Given** current active Owner or HR all-scope access, **when** the employee register is filtered or searched, **then** matching employees across all branches are returned with stable pagination.
2. **Given** a branch manager or supervisor, **when** employee lists or details are requested, **then** only employees currently assigned to the granted branch or department are visible and private fields are omitted.
3. **Given** an employee-linked account, **when** its own profile is requested, **then** only that employee's authorized profile is returned.
4. **Given** a missing or out-of-scope employee, **when** its detail is requested, **then** the same not-found outcome is returned without confirming existence.
5. **Given** revoked grants or a disabled account, **when** the next request is made, **then** stale access provides no employee disclosure.

---

### User Story 2 - Register and update an employee safely (Priority: P1)

HR and Owner create and maintain employee identity, contact details, and employment status. An employee must have a national or passport identifier; duplicates are rejected. Termination preserves the employee and their employment history.

**Why this priority**: Accurate identity and employment state are prerequisites for attendance, finance, and payroll.

**Independent Test**: Create a valid employee, update safe fields, reject duplicate and missing identity, and terminate without deleting the record.

**Acceptance Scenarios**:

1. **Given** valid identity and hire date, **when** HR or Owner creates an employee, **then** an active employee is returned with a unique employee code.
2. **Given** a duplicate employee code, national ID, or passport ID, **when** creation or update is attempted, **then** the existing record remains unchanged and a stable conflict is returned.
3. **Given** neither national nor passport ID, or a termination date earlier than hire date, **when** the request is submitted, **then** it is rejected with a field-level validation reason.
4. **Given** a terminated employee, **when** an authorized historical view is requested, **then** the employee and prior assignments remain available.
5. **Given** a scoped reader, **when** a mutation is attempted, **then** it is denied server-side.

---

### User Story 3 - Preserve assignment and compensation history (Priority: P1)

HR and Owner establish a first assignment and later transfer, promote, or change salary and welfare. Each change closes the prior effective period and starts a new row. Attendance and payroll consumers can resolve the exact assignment for a business date.

**Why this priority**: Historical branch, role, and pay must remain reproducible for past attendance and payslips.

**Independent Test**: Create an initial assignment, make an adjacent-dated change, query dates on each side, and reject overlapping or inconsistent organization paths.

**Acceptance Scenarios**:

1. **Given** an active employee and active branch, department, and position from a consistent organization path, **when** the initial assignment is created, **then** it takes effect on the specified business date.
2. **Given** an existing assignment, **when** a transfer, promotion, salary, or welfare change starts, **then** the prior row ends on the preceding date and a new row begins on the change date in one atomic decision.
3. **Given** an overlapping interval, an inactive master, a department outside the branch, or a position outside the branch's shop, **when** a new assignment is attempted, **then** no partial change is committed.
4. **Given** a past business date, **when** a downstream consumer asks for context, **then** the branch, department, position, employment type, base salary, and welfare valid on that date are returned without using the current assignment retrospectively.
5. **Given** a pay value, **when** it is submitted and returned, **then** exact two-decimal monetary values are preserved without floating-point rounding.

---

### User Story 4 - Maintain payroll bank accounts privately (Priority: P1)

HR and Owner manage encrypted employee bank accounts and primary selection. An employee can inspect only their own masked bank details. A bank account can be deactivated without erasing its history.

**Why this priority**: Payroll exports require a current destination while account numbers are highly sensitive.

**Independent Test**: Add two accounts, switch primary, deactivate one, verify one active primary at most and that responses and audit contain only masked details.

**Acceptance Scenarios**:

1. **Given** a new bank account, **when** HR or Owner submits it, **then** the account number is stored encrypted and only its last four digits are disclosed in ordinary responses and audit.
2. **Given** two active accounts, **when** primary status is switched, **then** at most one remains active primary and the change is atomic.
3. **Given** a primary account, **when** deactivation is requested, **then** the caller either selects an active replacement or explicitly accepts no primary.
4. **Given** a branch manager or supervisor, **when** bank data is requested, **then** access is denied even if the employee is in their team.

---

### User Story 5 - Maintain weekly holiday history (Priority: P1)

HR and Owner set effective-dated weekly holidays and end them when schedules change. Historical dates continue to resolve against the holiday rule that applied then.

**Why this priority**: Attendance and rest-day overtime need accurate date-based schedule context.

**Independent Test**: Create weekday rules at 0 and 6, end and replace one, and reject an overlapping same-weekday period.

**Acceptance Scenarios**:

1. **Given** a weekday from 0 through 6 and a valid effective date, **when** a rule is added, **then** it is available for the stated period.
2. **Given** an existing rule for the same weekday, **when** a replacement starts, **then** the earlier period is closed without rewriting its start date.
3. **Given** a negative weekday, a weekday above 6, reversed dates, or an overlapping same-weekday period, **when** the request is submitted, **then** it is rejected without changing prior history.

---

### User Story 6 - Complete onboarding as one decision (Priority: P1)

HR and Owner can register an employee together with the first assignment and optional bank account, weekly holidays, and user account. A failed step leaves no partly onboarded employee.

**Why this priority**: The two-step HR workflow must not produce an employee who lacks the employment context needed by downstream systems.

**Independent Test**: Complete all options successfully, then force failure in each optional step and verify the whole onboarding decision rolls back.

**Acceptance Scenarios**:

1. **Given** valid identity and first assignment, **when** onboarding is submitted, **then** the employee and all selected options are created together.
2. **Given** an invalid organization path, duplicate account, bank conflict, holiday conflict, or audit failure, **when** onboarding is submitted, **then** no partial employee, assignment, bank, holiday, or account row remains.
3. **Given** a generated temporary password for an optional account, **when** onboarding succeeds, **then** it appears only in the one-time authorized response and never in audit or later reads.

### Edge Cases

- Adjacent effective periods are allowed; even a one-day overlap is rejected.
- A change effective on the first day of an existing assignment must not create a zero-day or reversed prior interval.
- A new assignment cannot use an inactive branch, department, position, or parent shop; existing history remains readable.
- Employee status and account login status remain separate.
- An employee may have no active primary bank account only when the relevant command explicitly permits it.
- Bank plaintext, ciphertext, full identity identifiers, passwords, and tokens never appear in team-facing responses, audit snapshots, or logs.
- Employee attachments, OCR, and external clock integration are outside A3.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide filtered, searchable, paginated employee lists and safe detail views.
- **FR-002**: The system MUST enforce current Owner/HR all-branch, branch-manager branch, supervisor department, and employee self scope on every read; out-of-scope detail MUST appear not found.
- **FR-003**: Team readers MUST NOT receive compensation history, full national/passport identifiers, or bank details; own-profile and HR/Owner views MUST follow the approved field matrix.
- **FR-004**: Only current Owner/HR all-scope actors MUST create, update, change status, or manage assignments, bank accounts, and weekly holidays.
- **FR-005**: Employee code MUST be unique and at most 30 characters; at least one of national ID (at most 20 characters) or passport ID (at most 30 characters) MUST be present and each supplied identifier MUST be unique.
- **FR-006**: Employee name, contact, hire date, status, and termination date MUST meet the approved data model; termination MUST NOT delete the employee and its date MUST NOT precede hire date.
- **FR-007**: Assignment changes MUST end the preceding effective row and create a new row while preserving earlier branch, department, position, employment type, salary, and welfare facts.
- **FR-008**: An employee's assignment periods MUST NOT overlap; effective end MUST be on or after effective start.
- **FR-009**: New assignments MUST use active organization masters with a department in the selected branch and a position in that branch's shop.
- **FR-010**: Base salary and welfare MUST be exact, nonnegative two-decimal values within the approved numeric precision and remain distinct.
- **FR-011**: The system MUST resolve an employee's assignment and compensation for an arbitrary business date for downstream attendance and payroll consumers.
- **FR-012**: Bank account numbers MUST be encrypted before storage, and ordinary responses and audit MUST expose no more than the last four digits.
- **FR-013**: At most one active primary bank account MUST exist per employee; primary switches and deactivation MUST be atomic and preserve inactive history.
- **FR-014**: Deactivation of a primary account MUST require an active replacement or an explicit command to leave no primary.
- **FR-015**: Weekly holidays MUST use weekdays 0 through 6 and non-overlapping effective periods per employee and weekday; a replacement MUST preserve prior rows.
- **FR-016**: Onboarding MUST atomically create the employee and first assignment with selected optional bank, holiday, and account components, including one-time temporary credential handling.
- **FR-017**: Employee and account status MUST remain independent; a status change in one MUST NOT silently change the other.
- **FR-018**: Every public A3 action, including reads and failures, MUST emit one correlated redacted audit outcome; successful mutations and their audit facts MUST commit together.
- **FR-019**: The system MUST return stable safe errors for duplicate identity, organization mismatch, effective-date overlap, primary-bank conflict, validation, authorization, and state conflict.
- **FR-020**: The feature MUST preserve the existing organization/employee schema and historical relationships without public hard-delete operations.
- **FR-021**: Public identifiers MUST be decimal strings; dates MUST be business dates; money MUST be decimal strings in external contracts.
- **FR-022**: The feature MUST export independently composable routes and a downstream date-based context service without modifying the shared application composition file.
- **FR-023**: Focused tests MUST cover all five roles, historical date boundaries, overlap, inactive masters, identity uniqueness, money precision, masked bank data, one-primary behavior, weekly-holiday boundaries, atomic rollback, and audit redaction.

### Key Entities *(include if feature involves data)*

- **Employee**: Personal identity, contacts, hire date, and employment state, separate from any login account.
- **Employment Assignment**: Effective-dated organization placement and exact compensation.
- **Employee Bank Account**: Encrypted payroll destination, last-four display, active and primary states.
- **Employee Weekly Holiday**: Effective-dated recurring weekday off.
- **User Account**: Optional login identity linked to one employee, with its own status and grants.
- **Audit Fact**: Append-only, redacted evidence of each action outcome.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An authorized HR user can complete employee onboarding with a first assignment and chosen options in one submission, with zero partial records when any step fails.
- **SC-002**: Across the five-role access matrix, no tested user receives employee data or sensitive fields outside their authorized scope.
- **SC-003**: A transfer or pay change leaves the prior period intact, and date-based queries on either side return the correct branch and compensation in every boundary fixture.
- **SC-004**: Every tested bank account response and audit fact reveals at most the last four account digits, while zero plaintext account numbers are persisted.
- **SC-005**: One hundred percent of tested A3 endpoint invocations have exactly one correlated audit outcome; every forced audit failure rolls back its business mutation.
- **SC-006**: Employee list filters return a correct, stable page from at least 1,000 records within two seconds in the standard test environment.

## Assumptions

- A1 supplies current account status, active grants, transaction support, and audit observers; A2 supplies active organization masters and scoped organization context.
- Employee attachments and their storage are deferred.
- The existing PostgreSQL and Drizzle schemas remain the data-model baseline; schema mismatches are raised with the schema owner before migration changes.
- Historical assignment and holiday periods use inclusive business dates; a change on date D closes the old period on D minus one day.
- Bank encryption key sourcing and rotation are technical decisions to resolve in the implementation plan; the user-facing guarantee is no plaintext persistence or disclosure.
