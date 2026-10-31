# Research: Schedules and Attendance

## Applicable-schedule precedence

**Decision**: Resolve an active date-specific override first. If none exists, use
the branch schedule whose inclusive effective range contains the work date. Return
an explicit no-schedule result when neither exists.

**Rationale**: An override is a deliberate exception for one date. The PostgreSQL
exclusion constraint makes the normal schedule unambiguous for that date.

**Alternatives considered**: Combining override and normal values was rejected
because an override can declare the branch closed.

## Override validation

**Decision**: A closed override has no working hours. A non-closed override has both
start and close values, with close later than start on the same date.

**Rationale**: The frozen schema permits nullable hours but cannot distinguish a
deliberate closure from an incomplete open-day override.

## Stable conflicts

**Decision**: Services translate PostgreSQL unique/check/exclusion failures to
`SCHEDULE_RANGE_OVERLAP`, `SCHEDULE_OVERRIDE_EXISTS`, `HOLIDAY_ALREADY_EXISTS`,
`WORK_DAY_ALREADY_EXISTS`, and `INVALID_CLOCK_RANGE`.

**Rationale**: The database remains the concurrency boundary; stable errors remain
the public contract.

## Attendance branch snapshot

**Decision**: Creation requires an explicit branch ID, validates the employee's
effective assignment on the work date via Person A's service, then stores that ID.
Corrections never replace the branch ID.

**Rationale**: Payroll must use the historical branch after an employee transfer.

## Locking and transactions

**Decision**: B1 single-row writes are atomic. Attendance corrections call Person
C's payroll-lock guard before update. Later leave approval waits for C's shared
unit-of-work helper because it changes multiple records.

**Rationale**: The frozen schema has no trigger blocking attendance updates after a
payroll period locks.

## Verification approach

**Decision**: Service tests use injected repository and authorization dependencies;
opt-in PostgreSQL tests verify existing exclusion, uniqueness, clock-order and
snapshot storage safeguards.
