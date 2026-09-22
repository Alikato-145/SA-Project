# Quickstart: Validate PostgreSQL Infrastructure Alignment

## Prerequisites

- Bun 1.3.x
- Docker with Compose v2
- Ports 55432 and 8080 available for the isolated development check
- A completed implementation of this feature

These commands use an isolated Compose project so existing developer volumes are
not modified.

## 1. Static Validation

From the repository root:

```bash
git submodule status
cd backend
bun install --frozen-lockfile
bun run typecheck
bun test
```

Search supported source/configuration paths for stale active MySQL references:

```bash
if rg -n 'mysql2|mysql-core|mysql://|dialect: "mysql"|drizzle/mysql' \
  package.json drizzle.config.ts .env.example README.md src ../compose.yaml \
  ../compose.production.yaml ../README.md; then
  printf '%s\n' 'Unexpected active MySQL reference found'
  exit 1
fi
```

Expected: no active MySQL driver, schema import, URL, dialect, migration path, or
supported workflow reference. Historical notes explicitly labeled as legacy are
allowed only when they explain manual recovery.

## 2. Scope Validation

Review changed paths in the root and both submodules against their feature base:

```bash
git diff --name-only origin/main...HEAD
git -C backend diff --name-only origin/main...HEAD
git -C frontend diff --name-only origin/main...HEAD
```

Expected: changes are limited to database infrastructure, schema, migrations,
configuration, container setup, and documentation. No new business route,
controller, service, repository, API endpoint, or frontend UI source is present.

## 3. Migration Generation Check

From `backend/` with a valid development `DATABASE_URL`:

```bash
bun run db:generate
git status --short drizzle src
```

Expected: generation does not create an unexplained migration. If it does, inspect
the SQL and reconcile DBML, schema, and migration metadata before continuing.

## 4. Clean Development Stack

From the repository root:

```bash
cp .env.example .env
POSTGRES_PORT=55432 HTTP_PORT=8080 docker compose \
  -p haris-payroll-spec up --build -d
POSTGRES_PORT=55432 HTTP_PORT=8080 docker compose \
  -p haris-payroll-spec ps
curl --fail http://127.0.0.1:8080/healthz
curl --fail http://127.0.0.1:8080/api
```

Expected: PostgreSQL, backend, frontend, and gateway become healthy; the API root
returns the current backend response.

## 5. Catalog Verification

```bash
POSTGRES_PORT=55432 HTTP_PORT=8080 docker compose \
  -p haris-payroll-spec exec -T postgres \
  psql -U postgres -d haris_payroll -Atc \
  "select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE';"

POSTGRES_PORT=55432 HTTP_PORT=8080 docker compose \
  -p haris-payroll-spec exec -T postgres \
  psql -U postgres -d haris_payroll -Atc \
  "select count(*) from pg_type t join pg_namespace n on n.oid=t.typnamespace where n.nspname='public' and t.typtype='e';"
```

Expected: `36` public domain tables and `22` public enum types. Then run the focused
integration test to verify names, partial indexes, exclusions, and triggers rather
than relying on counts alone:

```bash
cd backend
TEST_DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:55432/haris_payroll \
  bun test src/core/db/database.integration.test.ts
```

## 6. Idempotence

```bash
POSTGRES_PORT=55432 HTTP_PORT=8080 docker compose \
  -p haris-payroll-spec restart backend
POSTGRES_PORT=55432 HTTP_PORT=8080 docker compose \
  -p haris-payroll-spec ps
```

Expected: migration re-run succeeds without duplicate objects or a second entry for
the same migration, and the backend returns to healthy.

## 7. Failure Safety

From `backend/`:

```bash
DATABASE_URL=mysql://legacy:secret@127.0.0.1:3306/haris_payroll \
  bun run src/index.ts
```

Expected: startup exits non-zero with PostgreSQL migration guidance and does not
print `legacy`, `secret`, or the full URL. Repeat with an unreachable PostgreSQL URL
and confirm that backend startup remains blocked.

## 8. Production Configuration Parity

Create an untracked `.env.production` from `.env.production.example`, set explicit
non-default secrets, then validate and start the production-like stack:

```bash
docker compose --env-file .env.production \
  -f compose.production.yaml config
docker compose --env-file .env.production \
  -f compose.production.yaml -p haris-payroll-production-spec up --build -d
docker compose --env-file .env.production \
  -f compose.production.yaml -p haris-payroll-production-spec ps
```

Expected: the same migration history produces the same table, enum, constraint,
index, and trigger inventory as development.

## 9. Cleanup

After validation, remove only the isolated environments created above:

```bash
POSTGRES_PORT=55432 HTTP_PORT=8080 docker compose \
  -p haris-payroll-spec down -v
docker compose --env-file .env.production \
  -f compose.production.yaml -p haris-payroll-production-spec down -v
```

These commands do not target legacy MySQL volumes or the normal development project.
