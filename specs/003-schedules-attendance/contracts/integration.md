# B1 Integration Contract

## Required from Person A

- Authenticated actor with account ID, role scope, and authorized branch/department values.
- Server-side authorization for all, branch, department and self scopes.
- Employee/effective-assignment lookup for a supplied employee/date, so a target
  historical branch is checked without reading a current assignment.

## Required from Person C

- Compose Person B's exported routes in `backend/src/app.ts` below `/api`.
- Translate B1 public error codes through the shared HTTP error boundary.
- Confirm shared API ID serialization and date/timestamp formats.
- Provide a read-only payroll-lock guard that corrections call before update.
- Make payroll consume the B1 range-reader with employee, work date, status,
  historical branch, clock times, lateness, deduction flag and source.

## B1 exports for Person C

Compose these factories below `/api`; each is intentionally unmounted and requires
an `actorFromContext` adapter from C's authenticated request context:

- `createBranchScheduleRoutes` from
  `backend/src/features/branch-schedule/branch-schedule.routes.ts`
- `createHolidayCalendarRoutes` from
  `backend/src/features/holiday-calendar/holiday-calendar.routes.ts`
- `createAttendanceRoutes` from
  `backend/src/features/attendance/attendance.routes.ts`

Each controller delegates server-side scope checks through injected interfaces.
Person A supplies the branch/shop and effective-assignment adapters; C supplies the
payroll-lock guard used before a work-day correction. C's shared error boundary must
render these public B1 codes: `SCHEDULE_RANGE_OVERLAP`,
`SCHEDULE_OVERRIDE_EXISTS`, `INVALID_OVERRIDE_HOURS`, `SCHEDULE_NOT_FOUND`,
`HOLIDAY_ALREADY_EXISTS`, `HOLIDAY_NOT_FOUND`, `WORK_DAY_ALREADY_EXISTS`,
`INVALID_CLOCK_RANGE`, `ATTENDANCE_NOT_FOUND`, `OUT_OF_SCOPE`, and
`PAYROLL_PERIOD_LOCKED`.

The attendance range reader accepts an employee and/or branch plus inclusive
`startDate`/`endDate`, and returns the stored work date, status, historical branch,
clock times, lateness, deduction flag, entry source, and note. It does not resolve a
current assignment while reading historical records.

## Remaining integration limits

- Routes cannot be mounted until C provides authenticated actor context and shared
  public-error translation.
- Corrections call the injected payroll-lock guard; C must wire it to the
  authoritative payroll-period state before exposing corrections.
- Manual attendance creation calls the injected effective-assignment lookup; A must
  supply it before route composition.

## Ownership boundary

Person B does not edit shared composition, authentication, authorization
infrastructure, payroll, employee/assignment features, schema or migrations. B1
routes remain unmounted until C supplies the shared actor/error contracts.
