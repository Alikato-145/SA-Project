# Haris Payroll

Start with [sprint readiness](docs/sprint-readiness.md), then follow the
[two-week plan for three developers](docs/two-week-three-person-plan.md).
PostgreSQL 16 is the supported database. The schema and migrations are frozen
during feature work; report discrepancies to the sprint schema coordinator.

Current handoff documents:

- [System completion tasks](specs/012-system-completion/tasks.md)
- [Role-based web user guide](docs/user-guide-by-role.md)
- [Release checklist](docs/release-checklist.md)

For an existing clone, first inspect `git status` in the root and both submodules.
A leading `+` from `git submodule status` means that checkout differs from the
root-recorded baseline. Preserve local work before synchronizing submodules.
For a fresh clone:

```bash
git submodule update --init --recursive
```

## Development with Hot Reload

The default `compose.yaml` runs the frontend and backend in watch mode. Source
directories are bind-mounted, while dependencies and the Next.js cache use
Docker volumes so they are not mixed with host files.

```bash
docker compose up --build -d --wait
docker compose ps
```

Run these commands from the root repository; there is no need to start Bun or
Compose separately in either submodule. Compose starts PostgreSQL, migrates the
database, and runs the backend, frontend, and gateway. Development defaults work
without environment files. To customize ports or secrets, create root `.env`
with `test -f .env || cp .env.example .env`; Docker does not require
`backend/.env` or `frontend/.env`.

Changes under `frontend/` and `backend/src/` reload automatically. Polling is
enabled for Next.js so file changes are detected through Docker Desktop bind
mounts on Windows and macOS as well as Linux.

After all health checks pass (replace the port if `HTTP_PORT` is customized):

- Frontend: <http://localhost>
- Backend: <http://localhost/api>
- Gateway health check: <http://localhost/healthz>

Only the gateway is publicly exposed. PostgreSQL is additionally bound to
`127.0.0.1:5432` for local database tools and is not reachable from other
machines. The frontend and backend communicate over the private
Compose project network. Networks and volumes are isolated by project name.

The backend applies pending PostgreSQL Drizzle migrations automatically before
starting. Do not point `DATABASE_URL` at MySQL: legacy MySQL volumes are not
read, changed, or removed by this stack.

For a fresh development database, create demo accounts and reference data once:

```bash
docker compose exec backend bun run db:seed
```

View application logs from the root with `docker compose logs -f backend frontend`.

If migration fails with `ENOTFOUND` for `postgres`, check the Compose network
attachments. Recreate the stack to restore container networking while keeping
database volumes:

```bash
docker compose up -d --force-recreate --wait
```

```bash
docker compose down       # stop containers, preserve database data
docker compose down -v    # stop containers and remove database data
```

Set `HTTP_PORT` and `POSTGRES_PORT` in your untracked `.env` if the defaults are
already in use. Never use `down -v` on a database whose history must be preserved.

Dependencies are synchronized into their Docker volumes when containers start.
Rebuild the development images after changing a `Dockerfile.dev`:

```bash
docker compose up --build
```

## Production

Production uses optimized images: the frontend runs as a Next.js standalone
server and the backend runs without watch mode. It has a separate network and
database volume from development.

Stop the development stack before starting production because both bind the
same HTTP port.

Create the untracked production environment file first. Production requires
explicit PostgreSQL credentials, a complete `DATABASE_URL`, `HTTP_PORT`, exact
allowed browser origins, a unique JWT secret, and a versioned AES-256-GCM
bank-account keyring; it has no development-secret fallbacks.

```bash
cp .env.production.example .env.production
docker compose --env-file .env.production -f compose.production.yaml up --build -d
docker compose --env-file .env.production -f compose.production.yaml down
```
