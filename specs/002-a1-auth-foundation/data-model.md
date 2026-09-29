# Data Model: A1 Authentication Foundation

This feature uses the existing frozen PostgreSQL model. No table, enum, column,
index, trigger, or migration is added by A1.

## User Account

Source: `user_accounts`

| Field | Meaning | A1 validation/use |
|---|---|---|
| `id` | Surrogate account identity | Serialized as a decimal string at API boundaries |
| `employee_id` | Optional unique employee link | One employee has at most one account; Owner may have no employee |
| `username` | Unique login name | Normalized comparison follows database uniqueness; never disclose existence on login failure |
| `password_hash` | Argon2id credential | Never returned, logged, or audited |
| `status` | `active`, `locked`, `disabled` | Admin transitions only active/disabled; login flow owns temporary locked state |
| `failed_login_attempts` | Consecutive failures | Non-negative; atomically updated under row lock |
| `locked_until` | Temporary lock expiry | Fifth failure sets now + 15 minutes |
| `last_login_at` | Last successful login | Set only on successful sign-in |

### Account state transitions

```text
active --5th consecutive failure--> locked
locked --lock expires + valid login--> active
locked --authorized admin unlock--> active
active/locked --authorized admin disable--> disabled
disabled --authorized admin enable--> active
```

Rules:

- A temporary lock never re-enables a disabled account.
- Successful sign-in clears failures and expired lock.
- Account disablement affects the next protected request even with an unexpired token.
- No hard-delete flow is exposed.

## Role

Source: `roles`

Exactly five controlled master records:

| Code | Scope | Meaning |
|---|---|---|
| `EMPLOYEE` | `self` | Own linked employee data |
| `SUPERVISOR` | `department` | One concrete branch and department |
| `BRANCH_MANAGER` | `branch` | One concrete branch |
| `HR` | `all` | All branches; manages A1-A3 except Owner grants |
| `OWNER` | `all` | All branches and all A1-A3 administration |

Role records are bootstrapped idempotently and are not user-editable in A1.

## Account Role Grant

Source: `user_account_roles`

| General scope | `branch_id` | `department_id` | Rule |
|---|---|---|---|
| `self` | null | null | Account must have an employee link to authorize employee-self targets |
| `department` | required | required | Department must belong to branch |
| `branch` | required | null | Authorizes permitted actions within that branch |
| `all` | null | null | HR/Owner all-branch scope |

Other rules:

- Duplicate logical grants are rejected.
- Inactive roles do not authorize and cannot receive new grants.
- Multiple valid grants form a union; any one grant may authorize a target.
- HR cannot grant/revoke `OWNER`; Owner may administer all roles.
- The final active Owner grant/account cannot be disabled or revoked.
- Revocation removes the junction row but its action remains in append-only audit.

## Authenticated Actor

Application projection, not a new table:

```text
account_id
employee_id | null
username
grants[]:
  grant_id
  role_code
  scope
  branch_id | null
  department_id | null
capabilities[]
```

It is reconstructed from current database state on each protected request. It never
contains a password hash, failed-attempt count, bank data, or full personal identifier.

## Session Token

Signed transient value, not persisted:

```text
sub = account id as decimal string
iat = issued-at time
exp = issued-at + 8 hours
```

Roles, scopes, status, username, and employee data are deliberately excluded.

## Audit Fact

Source: `audit_logs`

| Field | A1 convention |
|---|---|
| `actor_user_account_id` | Current actor or null for unknown authentication/system setup |
| `action` | `<domain>.<resource>.<verb>.<succeeded|failed>`, max 80 chars |
| `table_name` | Logical persistence target such as `user_accounts` |
| `record_id` | Decimal ID string or `unknown`, `self`, `collection` |
| `old_data` / `new_data` | Event-specific redacted allowlist snapshots |
| `reason` | Stable public reason/error code only; no raw exception |
| `occurred_at` | Database event time |
| `request_id` | Valid client correlation value or generated UUID |

### Audit transitions

Audit facts have no application update/delete transition. A successful mutation and
its fact commit together. A failed action appends a separate fact after rollback.
For invalid login, the attempt-count/lock mutation and failed outcome fact commit
together because the failure intentionally changes account state.

## Related scope entities

- `employees`: optional account link and self-scope target.
- `branches`: branch-scope target and required parent for department scope.
- `departments`: department-scope target; must belong to the submitted branch.

A1 reads these entities for validation/projection but does not own their CRUD.
