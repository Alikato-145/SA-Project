# Feature Specification: Schedules and Attendance

**Feature Branch**: `main`

**Created**: 2026-09-22

**Status**: Draft

**Input**: User description: "You are Person B. Implement work package B1, Schedules and Attendance, from docs/two-week-three-person-plan.md. Follow AGENTS.md. Do not change the database schema, migrations, shared application files, or work owned by Persons A and C. Add appropriate tests and report any integration changes needed from Person C."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Maintain a branch's working schedule (Priority: P1)

An authorized branch manager can define the normal working schedule for their
branch and set a one-day exception, so attendance has a reliable expected start
and close time for every working date.

**Why this priority**: Attendance cannot be recorded consistently until the
applicable schedule is known.

**Independent Test**: Create an effective-dated schedule and a date-specific
override, then retrieve the applicable schedule for dates before, on, and after
the override.

**Acceptance Scenarios**:

1. **Given** a branch has no conflicting schedule, **When** an authorized manager
   creates a schedule with an effective date range, **Then** that schedule is
   available for dates in its range.
2. **Given** a branch has an active schedule, **When** an authorized manager
   records a closed-day or changed-hours override for one date, **Then** the
   override takes precedence on that date only.
3. **Given** a manager attempts to create a schedule whose date range overlaps
   another active schedule for the branch, **When** it is submitted, **Then** the
   system rejects it and preserves the existing schedule.

---

### User Story 2 - Maintain the shop holiday calendar (Priority: P2)

An authorized manager can identify an active public holiday for a shop, so the
attendance and payroll process can distinguish it from an ordinary working day.

**Why this priority**: A holiday changes the expected attendance outcome for every
branch in the shop.

**Independent Test**: Create an active holiday, retrieve it by shop and date, then
deactivate it and verify that it is no longer returned as active.

**Acceptance Scenarios**:

1. **Given** a shop does not already have a holiday on a date, **When** an
   authorized manager records the holiday, **Then** the date and its name are
   available to all branches of that shop.
2. **Given** an inactive holiday entry, **When** attendance is checked for its
   date, **Then** it is treated as an ordinary date.

---

### User Story 3 - Record and correct manual attendance (Priority: P3)

An authorized manager can record one employee's attendance for one work date and
correct it before payroll is locked, while preserving the branch where the work
was performed as a historical fact.

**Why this priority**: Complete attendance is required before payroll can be
calculated and locked.

**Independent Test**: Record a work day for an employee, change that employee's
current assignment context, and verify that the recorded branch remains unchanged.

**Acceptance Scenarios**:

1. **Given** an employee and a work date without attendance, **When** an
   authorized manager records manual attendance with a branch, **Then** exactly
   one work-day record exists for that employee and date with that branch.
2. **Given** a work-day record created before an employee transfers, **When** the
   employee's current assignment changes later, **Then** the prior attendance
   continues to show the original recorded branch.
3. **Given** a work-day record is still editable, **When** an authorized manager
   corrects its status or clock times, **Then** the same record is updated without
   creating a second record for the date.

### Edge Cases

- A schedule has an open-ended effective range and a later schedule is added.
- An override declares the branch closed and does not provide working hours.
- A holiday is entered twice for the same shop and date.
- A manual record is submitted twice for the same employee and date.
- A clock-out time is earlier than the clock-in time.
- An attendance date has no applicable schedule or uses an inactive holiday.
- A request falls outside the actor's branch scope.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow authorized actors to create, retrieve, and
  update effective-dated branch schedules within their permitted branch scope.
- **FR-002**: The system MUST reject overlapping active schedule ranges for the
  same branch and preserve the existing schedule data.
- **FR-003**: The system MUST allow one date-specific override per branch, including
  a closed day or replacement working hours, and apply it before the normal schedule.
- **FR-004**: The system MUST allow authorized actors to create, retrieve, and
  deactivate shop holiday entries within their permitted shop scope.
- **FR-005**: The system MUST prevent multiple holiday entries for the same shop and
  date and treat inactive entries as unavailable for attendance decisions.
- **FR-006**: The system MUST allow authorized actors to create, retrieve, and
  correct manual work-day records within their permitted branch scope.
- **FR-007**: The system MUST allow at most one work-day record for an employee and
  work date.
- **FR-008**: The system MUST store the branch selected when attendance is recorded
  and must not derive that historical value from a later employee assignment.
- **FR-009**: The system MUST reject clock times whose end precedes their start.
- **FR-010**: The system MUST identify manual entry as the source of records created
  through this feature.
- **FR-011**: The system MUST provide payroll consumers with the recorded status,
  work date, historical branch, clock times, and source for a selected date range.
- **FR-012**: The system MUST enforce authorization on the server; visual controls
  alone are not an authorization boundary.

### Key Entities *(include if feature involves data)*

- **Branch schedule**: The normal working hours, late grace allowance, and date
  range that apply to one branch.
- **Schedule override**: A one-date exception for one branch, which can change hours
  or declare that branch closed.
- **Holiday calendar entry**: An active or inactive named public holiday for a shop
  and date.
- **Work-day record**: One employee's attendance result for one date, including the
  branch where work occurred, clock times, status, and entry source.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A branch manager can record a normal schedule and a one-day exception
  for a branch in under two minutes.
- **SC-002**: For 100 tested dates, the applicable schedule outcome consistently
  gives precedence to a valid override over the normal schedule.
- **SC-003**: A manager can record and then retrieve one employee's attendance for a
  date without creating duplicate records in 100% of tested duplicate submissions.
- **SC-004**: After an employee assignment changes, 100% of previously recorded
  attendance samples retain their original work branch.
- **SC-005**: All tested out-of-scope attendance and scheduling requests are denied
  before they can change records.

## Assumptions

- Authentication, actor identity, scoped authorization helpers, stable public error
  mapping, employee records, assignments, and organization data are delivered by
  Persons A and C through their agreed service contracts.
- Until those dependencies are available, Person B validates behavior through
  repository and service tests using explicit actor and branch fixtures.
- Corrections are permitted only while the related payroll period has not been
  locked; the authoritative payroll-lock integration is owned by Person C.
- Manual attendance is the supported source in this sprint. Imports and biometric
  devices remain deferred.
- The frozen database model supplies uniqueness and effective-range protections;
  no schema or migration change is part of this work package.
