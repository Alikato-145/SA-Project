# A2 Organization API Contract

## Conventions

- Base path: `/api/v1`
- Media type: `application/json`
- Persistence and API fields use `snake_case`.
- Public identifiers are decimal strings. Numbers that are unsafe, fractional,
  signed, exponent-formatted, empty, or outside the bigint range are invalid.
- List responses use `{ data, page, page_size, total }`.
- Detail and mutation responses use `{ data }`.
- Inactive records are excluded from lists unless `is_active=false` is supplied.
- There is no public `DELETE` endpoint for any organization resource.

## Common list query

| Field | Type | Default | Constraint |
|---|---|---:|---|
| `page` | integer | 1 | 1 or greater |
| `page_size` | integer | 20 | 1–100 |
| `search` | string | absent | trimmed, max 150, matches code or name |
| `is_active` | boolean | `true` | explicit `false` returns inactive-only rows |

Child lists additionally accept their immutable parent identifier:

- branches: `shop_id`
- departments: `branch_id`
- positions: `shop_id`

All filters are intersected with the authenticated actor's active organization
scope. A filter never expands scope.

Lists use deterministic ascending `(code, id)` ordering. An authenticated
detail request outside the actor's visible scope returns `RESOURCE_NOT_FOUND`
instead of disclosing that the record exists.

## Shops

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/shops` | List visible shops |
| `POST` | `/shops` | Create a shop (Owner/HR) |
| `GET` | `/shops/:shop_id` | Read a visible shop |
| `PATCH` | `/shops/:shop_id` | Update code/name (Owner/HR) |
| `POST` | `/shops/:shop_id/deactivate` | Deactivate with a reason (Owner/HR) |

Create body: `{ "code": string, "name": string }`

Update body: at least one of `{ "code"?: string, "name"?: string }`.

## Branches

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/branches` | List visible branches |
| `POST` | `/branches` | Create a branch (Owner/HR) |
| `GET` | `/branches/:branch_id` | Read a visible branch |
| `PATCH` | `/branches/:branch_id` | Update safe fields (Owner/HR) |
| `POST` | `/branches/:branch_id/deactivate` | Deactivate with a reason (Owner/HR) |

Create body:

```json
{
  "shop_id": "1",
  "code": "BKK-01",
  "name": "Bangkok Main",
  "address": "optional, maximum 500 characters",
  "timezone": "Asia/Bangkok"
}
```

Update body may contain `code`, `name`, `address`, or `timezone`. `shop_id` is
never accepted by the update contract.

## Departments

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/departments` | List visible departments |
| `POST` | `/departments` | Create a department (Owner/HR) |
| `GET` | `/departments/:department_id` | Read a visible department |
| `PATCH` | `/departments/:department_id` | Update code/name (Owner/HR) |
| `POST` | `/departments/:department_id/deactivate` | Deactivate with a reason (Owner/HR) |

Create body: `{ "branch_id": string, "code": string, "name": string }`.

Update body may contain `code` or `name`. `branch_id` is never accepted.

## Positions

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/positions` | List visible positions |
| `POST` | `/positions` | Create a position (Owner/HR) |
| `GET` | `/positions/:position_id` | Read a visible position |
| `PATCH` | `/positions/:position_id` | Update code/name (Owner/HR) |
| `POST` | `/positions/:position_id/deactivate` | Deactivate with a reason (Owner/HR) |

Create body: `{ "shop_id": string, "code": string, "name": string }`.

Update body may contain `code` or `name`. `shop_id` is never accepted.

## Deactivation

All four resources use:

```json
{ "reason": "non-empty audit reason, maximum 500 characters" }
```

Deactivation is one-way in A2. It changes only the selected row, does not
cascade to children, and returns `STATE_CONFLICT` if the row is already
inactive.

## Stable errors

| Code | Status | Meaning |
|---|---:|---|
| `AUTH_REQUIRED` | 401 | No valid A1 actor |
| `FORBIDDEN_SCOPE` | 403 | Actor cannot access or administer this scope |
| `RESOURCE_NOT_FOUND` | 404 | Visible target does not exist |
| `DUPLICATE_CODE` | 409 | Code uniqueness would be violated |
| `STATE_CONFLICT` | 409 | Parent is inactive or target cannot transition |
| `VALIDATION_ERROR` | 422 | Request shape, identifier, text, or timezone is invalid |

Errors use the shared public error envelope and never expose SQL, constraint
names, stack traces, or records outside the actor's scope.

## Audit actions

Each invocation produces exactly one correlated action outcome. Successful
mutations also produce an atomic domain change fact.

- `organization.shop.list|read|create|update|deactivate`
- `organization.branch.list|read|create|update|deactivate`
- `organization.department.list|read|create|update|deactivate`
- `organization.position.list|read|create|update|deactivate`

Audit snapshots are allowlisted to identifiers, code, name, active state, safe
parent identifiers, timezone, and address where applicable.

For create actions, the initial transport target is the `unknown` sentinel;
the generated identifier is retained in the allowlisted `new_data.id` domain
snapshot written in the same transaction as the new record.
