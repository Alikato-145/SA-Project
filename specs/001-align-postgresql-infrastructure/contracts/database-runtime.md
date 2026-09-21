# Database Runtime Contract

## Supported Database

- PostgreSQL 16 is the only supported database engine and dialect.
- Supported URL schemes are `postgres:` and `postgresql:`.
- MySQL URLs, services, drivers, schemas, and migration histories are unsupported.
- The canonical schema entry point is `backend/src/db/schema.ts`.
- The canonical ordered migration directory is `backend/drizzle/`.

## Environment Variables

| Context | Required values | Contract |
|---------|-----------------|----------|
| Root development Compose | `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_PORT`, `HTTP_PORT` | Development defaults may be supplied by `.env.example`; database port binds to loopback only. |
| Backend on host | `DATABASE_URL`, optional `ELYSIA_HOST`, optional `ELYSIA_PORT` | URL targets the root Compose PostgreSQL port and uses a supported scheme. |
| Production Compose | explicit `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `DATABASE_URL`, `HTTP_PORT` | No production password or database URL fallback; secrets are supplied outside version control. |

Passwords containing reserved URL characters must be percent-encoded when included
in `DATABASE_URL`. Validation and error output never print the full URL.

## Supported Commands

Run backend commands from `backend/`:

| Command | Expected behavior |
|---------|-------------------|
| `bun run db:generate` | Compare the PostgreSQL schema with canonical migration metadata and generate reviewed SQL only when the model changed. |
| `bun run db:migrate` | Apply pending migrations from `backend/drizzle/`; exit non-zero on connection or migration failure. |
| `bun run db:up` | Start and wait for the root PostgreSQL development service only. |
| `bun run db:down` | Stop the root PostgreSQL development service without deleting its volume. |
| `bun run typecheck` | Validate backend TypeScript without emitting files. |
| `bun test` | Run the focused database configuration and catalog checks; it is no longer a placeholder command. |

Run complete stacks from the repository root:

| Command | Expected behavior |
|---------|-------------------|
| `docker compose up --build` | Start PostgreSQL, migrate once for the backend process, then start backend, frontend, and gateway. |
| `docker compose -f compose.production.yaml up --build -d` | Require production secrets, apply the same migration history, and start the production-like stack. |

`db:push` is not part of the supported production workflow.

## Startup Ordering

```text
PostgreSQL healthy → backend migration succeeds → backend server starts
                                            ├── frontend starts
                                            └── gateway becomes available
```

The backend process must not start if migration fails. With the current single
backend process, the container entry command owns migration. If deployment later
uses multiple replicas, migration moves to a one-shot release job before replicas
start.

## Failure Behavior

- A MySQL URL fails before a database connection is attempted and points the
  developer to the PostgreSQL environment example.
- An unreachable PostgreSQL instance or failed migration exits non-zero and blocks
  backend startup.
- Errors may identify a variable name, URL scheme, host reachability category, or
  migration identifier, but never credentials or a complete connection URL.
- If a migration is interrupted or fails, backend startup remains blocked. Recovery
  follows the reviewed migration history; application code never attempts ad hoc
  schema repair.

## Legacy MySQL Safety

- No supported command automatically reads, converts, resets, or deletes a MySQL
  database or Docker volume.
- Developers with legacy local data must inspect or export it before manually
  removing the old environment.
- Migration of confirmed real MySQL data requires a separate specification and
  explicit validation; it is not part of this feature.

## Schema Acceptance Contract

A clean migrated database contains exactly the 36 expected domain tables and 22
named enums, plus migration bookkeeping outside the public domain-table count. It
also contains the documented partial indexes, exclusion constraints, validation
triggers, append-only protections, and locked-payroll protection described in
`../data-model.md`.
