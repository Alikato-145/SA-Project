# Operations HTTP Contract

All released operations endpoints are under `/api/v1/operations` and require the
existing session cookie. Mutations require the existing same-origin/CSRF policy.

## Contract rules

- Success responses use `{ "data": ..., "request_id": "..." }`.
- Error responses use `{ "error": { "code": "...", "message": "..." }, "request_id": "..." }`.
- The server derives the actor and its scope from the session; clients never
  submit role, scope, or actor account identifiers.
- IDs are decimal strings at the public boundary. Money stays decimal strings.
- A hidden or unauthorized record is returned as a safe authorization/not-found
  public error, without leaking its state.

## Released workflow families

| Family | User-facing purpose | Allowed scopes |
|---|---|---|
| Attendance | Read and manage daily work records | HR/Owner all scope; branch and department scope only for assigned records |
| Schedules and holidays | Manage operational calendar facts | HR/Owner all scope; branch/department only where assignment scope permits |
| Leave and overtime | Submit own requests; decide allowed requests | Employee self; supervisor department; branch manager branch; HR/Owner all |
| Advances, loans, debt | Request/read own finance and administer allowed employee finance | Employee self; supervisor/branch/HR/Owner only within their scope |

Exact endpoint payloads retain the existing feature DTO fields. C4 changes their
application prefix, authentication, safe envelope, and composition only; it does
not introduce new business fields.
