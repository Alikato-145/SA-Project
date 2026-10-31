# B4 UI/API Contract

| Screen | Read | Write |
|---|---|---|
| Attendance | `GET /api/work-day-records` | `POST /api/work-day-records`, `PATCH /api/work-day-records/:id` |
| Leave | `GET /api/leave-requests?employee_id=` | `POST /api/leave-requests`, `POST /api/leave-requests/:id/approve` or `/reject` |
| Overtime | `GET /api/overtime-records?employee_id=` | `POST /api/overtime-records`, decision routes |
| Finance | `GET /api/advance-requests`, `/loans`, `/debt-transactions` with `employee_id=` | POST request, decision, loan, debt, and reversal routes |

Person C must mount the backend plugins under `/api`, connect the authenticated actor and public error boundary, and link these routes from the dashboard navigation. The same-origin frontend proxy or deployment routing must send `/api` to the Elysia backend. Until C does this, pages compile but server calls cannot complete.
