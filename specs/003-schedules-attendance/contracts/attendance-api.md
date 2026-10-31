# B1 API Contract for Composition

Person B exports route modules. Person C mounts them below `/api` and provides
authenticated actor context and the shared error boundary. C confirms API-wide ID
serialization before route publication.

## Branch schedules

| Method and path | Request | Successful result |
|---|---|---|
| `POST /branch-schedules` | branch, normal hours, grace, effective range | Created schedule |
| `GET /branch-schedules` | branch and optional date filter | Matching schedules |
| `PATCH /branch-schedules/:id` | Allowed schedule correction | Updated schedule |
| `GET /branch-schedules/applicable` | branch and work date | Override, schedule, or no-schedule outcome |
| `PUT /branch-schedules/:branchId/overrides/:date` | closed-day or complete replacement hours | Stored override |

## Holiday calendar

| Method and path | Request | Successful result |
|---|---|---|
| `POST /holiday-calendars` | shop, date, name | Created holiday |
| `GET /holiday-calendars` | shop, optional date, active-only filter | Matching holidays |
| `PATCH /holiday-calendars/:id` | name and/or active status | Updated holiday |

## Attendance

| Method and path | Request | Successful result |
|---|---|---|
| `POST /work-day-records` | employee, historical branch, work date, status, optional clock values, late minutes, deduction flag, note | Created manual record |
| `GET /work-day-records` | employee and/or branch, bounded date range | Records with payroll input fields |
| `PATCH /work-day-records/:id` | Correctable status, clock, lateness, deduction flag, note | Updated record retaining original branch and source |

## Public error codes

`SCHEDULE_RANGE_OVERLAP`, `SCHEDULE_OVERRIDE_EXISTS`, `HOLIDAY_ALREADY_EXISTS`,
`WORK_DAY_ALREADY_EXISTS`, `INVALID_CLOCK_RANGE`, `INVALID_OVERRIDE_HOURS`,
`SCHEDULE_NOT_FOUND`, `ATTENDANCE_NOT_FOUND`, `OUT_OF_SCOPE`, and
`PAYROLL_PERIOD_LOCKED`.
