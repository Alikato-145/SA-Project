# Contract: A1 Authentication and Account API

Base path: `/api/v1`. JSON field names are `snake_case`. Bigint IDs are decimal
strings. Every response includes `request_id`; public failures use a stable error code.

## Envelope

```json
{"data": {}, "request_id": "019..."}
```

```json
{
  "error": {
    "code": "FORBIDDEN_SCOPE",
    "message": "You do not have permission to perform this action.",
    "field_errors": {}
  },
  "request_id": "019..."
}
```

## Authentication

### `POST /auth/login`

Request:

```json
{"username": "mana", "password": "not-returned"}
```

Success `200` sets `haris_session` and returns the safe current-actor DTO.

Errors: `INVALID_CREDENTIALS` (401), `ACCOUNT_DISABLED` (403),
`ORIGIN_NOT_ALLOWED` (403), `ACCOUNT_LOCKED` (423 with `retry_at`).

### `POST /auth/logout`

Idempotently expires `haris_session` and returns:

```json
{"data": {"logged_out": true}, "request_id": "..."}
```

### `GET /auth/me`

Returns:

```json
{
  "data": {
    "account": {
      "id": "12",
      "username": "mana",
      "status": "active",
      "employee": {
        "id": "45",
        "employee_code": "EMP-045",
        "display_name": "Mana Example"
      }
    },
    "grants": [
      {
        "id": "20",
        "role_code": "SUPERVISOR",
        "scope": "department",
        "branch_id": "2",
        "department_id": "8"
      }
    ],
    "capabilities": ["employee.read.department"]
  },
  "request_id": "..."
}
```

No credential, attempt counter, internal lock field, bank value, or full personal
identifier is returned.

## Account administration (HR/Owner)

### `GET /accounts`

Filters: `page`, `page_size`, `search`, `status`, `role_code`, `branch_id`,
`department_id`. Returns safe summaries and pagination.

### `POST /accounts`

```json
{"username": "somchai", "employee_id": "45"}
```

`employee_id` is optional. Success returns safe account plus
`temporary_password` exactly once. Initial role grants use the grant endpoint.

### `GET /accounts/:account_id`

Returns safe account detail, linked employee summary, and current grants.

### `PATCH /accounts/:account_id/status`

```json
{"status": "active", "reason": "Reactivated by HR"}
```

Only `active` and `disabled` are accepted. `locked` is controlled by authentication.
Disabling the final active Owner is rejected.

### `POST /accounts/:account_id/reset-password`

```json
{"reason": "Employee requested reset"}
```

Success returns a newly generated `temporary_password` once. Existing stateless
tokens remain valid until expiry unless the account is also disabled.

### `POST /accounts/:account_id/unlock`

```json
{"reason": "Identity verified"}
```

Sets active status, zero attempts, and clears lock time atomically. It does not
enable a disabled account unless the separate status action is authorized.

## Role administration

### `GET /roles`

Returns the five fixed role records. No role create/update/delete endpoint exists.

### `POST /accounts/:account_id/roles`

```json
{
  "role_code": "SUPERVISOR",
  "branch_id": "2",
  "department_id": "8",
  "reason": "Promoted to supervisor"
}
```

Valid shapes follow `data-model.md`. HR cannot grant Owner. A caller cannot grant
authority beyond their own current authority.

### `DELETE /accounts/:account_id/roles/:grant_id`

Verifies the grant belongs to the path account and preserves evidence in audit.
Removing the final active Owner authority is rejected.

## Audit query (HR/Owner)

### `GET /audit-logs`

Filters: `page`, `page_size`, `action`, `actor_account_id`, `table_name`,
`record_id`, `request_id`, `occurred_from`, `occurred_to`.

Returns redacted audit DTOs only. Querying audit is itself observed without recursively
auditing the audit repository insert.

## Public error mapping

| HTTP | Codes |
|---:|---|
| 400 | `MALFORMED_REQUEST` |
| 401 | `AUTH_REQUIRED`, `INVALID_CREDENTIALS` |
| 403 | `ACCOUNT_DISABLED`, `FORBIDDEN_SCOPE`, `ORIGIN_NOT_ALLOWED` |
| 404 | `RESOURCE_NOT_FOUND` |
| 409 | `DUPLICATE_USERNAME`, `EMPLOYEE_ACCOUNT_ALREADY_EXISTS`, `DUPLICATE_ROLE_GRANT`, `STATE_CONFLICT` |
| 422 | `VALIDATION_ERROR`, `INVALID_ROLE_SCOPE`, `INVALID_ORGANIZATION_RELATION` |
| 423 | `ACCOUNT_LOCKED` |
| 500 | `INTERNAL_ERROR` |

Unknown internal messages, SQL text, stack traces, credentials, and existence hints
must never be placed in the public response.
