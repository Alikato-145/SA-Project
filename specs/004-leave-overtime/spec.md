# Feature Specification: Leave and Overtime

**Feature Branch**: `main`

**Created**: 2026-09-22

**Status**: Draft

**Input**: User description: "B2"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Submit and approve leave (Priority: P1)

An employee submits a dated leave request, and an authorized supervisor or branch
manager approves or rejects it so attendance and pay reflect the decision.

**Why this priority**: Approved leave must be distinguished from absence before
payroll is calculated.

**Independent Test**: Submit a two-day request, approve it with an authorized
supervisor, and verify the days, quota use, attendance outcome, and approval record.

**Acceptance Scenarios**:

1. **Given** an employee has available entitlement and no overlapping request,
   **When** they submit leave dates, **Then** the request is pending with one
   recorded day per date.
2. **Given** a pending request for three days or fewer, **When** an authorized
   supervisor approves it, **Then** the request is approved and its quota and
   attendance effects are recorded together.
3. **Given** a pending request longer than three days, **When** a supervisor tries
   to approve it, **Then** it remains pending; a branch manager may approve it.

---

### User Story 2 - Preserve leave decisions and corrections (Priority: P2)

An authorized approver can reject a request or correct its requested leave type
while deciding it, with a permanent decision history.

**Why this priority**: Payroll and later reviews need to know both the requested
and final leave classification and who made each decision.

**Independent Test**: Submit a request, approve it using a corrected leave type,
then verify the original type, final type, and ordered decision history.

**Acceptance Scenarios**:

1. **Given** a pending leave request, **When** an authorized approver changes its
   leave type while approving, **Then** the final type drives quota and attendance
   effects while the requested type remains visible.
2. **Given** a pending request, **When** an authorized approver rejects it,
   **Then** no quota or attendance effect is created and the rejection is recorded.

---

### User Story 3 - Request and explicitly approve overtime (Priority: P3)

An employee or authorized manager submits overtime, and an authorized approver
explicitly approves or rejects it before payroll can treat it as payable.

**Why this priority**: A late clock-out alone must never create payable overtime.

**Independent Test**: Submit one hourly, one rest-day, and one public-holiday OT
request; approve only one and verify payroll sees only the approved request.

**Acceptance Scenarios**:

1. **Given** an eligible work date, **When** a request is submitted with an OT
   type and matching amount, **Then** it is pending and not payable.
2. **Given** a pending OT request, **When** an authorized approver approves it,
   **Then** it becomes payable and has an append-only approval record.
3. **Given** a duplicate OT request for an employee and date, **When** it is
   submitted, **Then** the existing record is preserved and the duplicate is denied.

### Edge Cases

- Leave dates overlap a pending or approved request for the same employee.
- Leave exceeds remaining entitlement where the leave type does not allow excess.
- A supervisor approves three days versus four days.
- Approval is attempted after a request was already decided.
- Hourly OT supplies day units, or rest-day/public-holiday OT supplies hours.
- An OT request is submitted for a date that has no qualifying attendance context.
- An out-of-scope actor attempts to view, submit, or decide another employee's item.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST let authorized actors submit dated leave requests
  without overlapping leave days for the same employee.
- **FR-002**: The system MUST create leave day records for every submitted date and
  retain the requested leave type.
- **FR-003**: The system MUST enforce leave entitlement and prevent quota use above
  the permitted amount unless the leave type allows excess.
- **FR-004**: The system MUST allow a supervisor to approve up to three requested
  days and require a branch manager for longer requests.
- **FR-005**: The system MUST allow a branch manager to approve a request directly.
- **FR-006**: The system MUST apply leave approval, quota use, and attendance
  updates as one decision so partial effects are never visible.
- **FR-007**: The system MUST retain append-only leave decision history, including a
  change from requested to final leave type.
- **FR-008**: The system MUST let authorized actors submit hourly, rest-day, and
  public-holiday OT requests with the amount appropriate to that type.
- **FR-009**: The system MUST require an explicit OT approval before an OT request
  is payable and retain append-only OT decision history.
- **FR-010**: The system MUST prevent more than one OT request for an employee and
  work date.
- **FR-011**: The system MUST enforce employee, department, and branch scope on all
  leave and OT actions.
- **FR-012**: The system MUST provide payroll consumers the final approved leave and
  OT values with their decision state and historical work-date context.

### Key Entities *(include if feature involves data)*

- **Leave request**: An employee's dated request, its requested and final type,
  decision state, and stated reason.
- **Leave quota**: The employee's annual entitlement and recorded use for a leave
  type.
- **Leave decision**: An immutable record of a submission, approval, rejection, or
  approved type correction.
- **Overtime request**: A dated requested amount and type with a decision state.
- **Overtime decision**: An immutable approval or rejection record for overtime.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An authorized employee can submit a valid two-day leave request in
  under two minutes.
- **SC-002**: All tested leave decisions either apply every required effect or
  apply none of them.
- **SC-003**: In tested three-day and four-day cases, supervisors approve 100% of
  eligible requests and are denied 100% of ineligible ones.
- **SC-004**: In tested OT requests, 100% of payroll-visible overtime has an
  explicit approval; no pending or rejected request is payable.
- **SC-005**: In 100 duplicate-request attempts for the same employee/date, the
  system preserves exactly one leave day or OT record as applicable.

## Assumptions

- Existing leave types, quotas, employee assignments, attendance records, and role
  scopes are available from their owning work packages.
- Requests are submitted in whole calendar days for this sprint; the stored daily
  amount supports future partial-day policy without adding it to this scope.
- A qualifying attendance, rest-day, or public-holiday context is supplied to OT
  validation by the attendance and calendar services.
- Schema and migrations remain frozen. Payroll composition and shared authorization
  infrastructure are integration work owned by Persons A and C.
