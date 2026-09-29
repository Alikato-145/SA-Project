# Contract: A1 Audit Observer

## Coverage boundary

Observed:

- Every `/api/v1` A1 business endpoint invocation.
- Successful reads and mutations.
- Validation, authentication, authorization, state, and persistence failures.
- Login/logout, including actor-null failures.

Excluded to avoid noise or recursion:

- Health checks, static files, CORS preflight, unknown routes.
- The internal audit repository insert itself.
- UI interactions that do not call a backend use case.

## Canonical event rule

Exactly one canonical audit row is expected for each observed endpoint invocation.

- Mutation success: transactional domain audit is canonical.
- Read success: action observer appends before returning data.
- Failure with no intentional state change: append after rollback.
- Invalid login: counter/lock change plus failed outcome audit commit together.

## Action context

```text
request_id: validated <=100-character correlation ID or generated UUID
actor_user_account_id: bigint string or null
action_base: stable domain.resource.verb
target.table_name: approved logical table name
target.record_id: bigint string or unknown/self/collection
```

Observer appends `.succeeded` or `.failed`; the final value must fit 80 characters.

## Mutation contract

```text
begin transaction
  load/validate/authorize
  capture allowlisted old facts
  apply business mutation
  capture allowlisted new facts
  append canonical audit row using the same transaction executor
commit
```

If audit append fails, the transaction fails. A mutation service may not return a
successful result without an audit receipt.

## Failure contract

After the business transaction has rolled back, append a row through the root database
executor with the stable public error code only. Re-throw the original application
error. If the audit store is unavailable, emit a redacted operational fallback and do
not claim durable audit persistence.

## Read contract

Load and authorize data, append the read outcome, then return. If required audit
persistence fails, do not disclose the requested protected data.

## Redaction contract

Primary control: per-action allowlist builders.

Defense-in-depth forbidden keys/patterns include:

```text
password
temporary_password
password_hash
token
jwt
cookie
authorization
secret
account_number
account_number_ciphertext
national_id
passport_id
```

Nested objects and arrays are scanned recursively. Raw headers, bodies, thrown errors,
and database row objects are never accepted directly by the audit repository.

## Required tests

- One row for mutation success with commit and no duplicate observer row.
- Audit insert failure rolls back the mutation.
- Business constraint failure rolls back, then its failure row persists.
- Read success/failure is observed before disclosure.
- Validation failure before controller is observed.
- Authentication/authorization failure is observed.
- Invalid login counter and failure audit commit atomically.
- Redaction covers nested objects, arrays, mixed-case keys, and all prohibited values.
- Audit update/delete is rejected by existing append-only protection.
- Audit query produces one non-recursive observed event.
