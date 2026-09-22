# Haris Payroll

Start with [sprint readiness](docs/sprint-readiness.md), then follow the
[two-week plan for three developers](docs/two-week-three-person-plan.md).
PostgreSQL 16 is the supported database. The schema and migrations are frozen
during feature work; report discrepancies to the sprint schema coordinator.

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
cp .env.example .env
docker compose up --build -d
docker compose ps
```

Changes under `frontend/` and `backend/src/` reload automatically. Polling is
enabled for Next.js so file changes are detected through Docker Desktop bind
mounts on Windows and macOS as well as Linux.

After all health checks pass:

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
explicit PostgreSQL credentials, a complete `DATABASE_URL`, and `HTTP_PORT`;
it has no development-secret fallbacks.

```bash
cp .env.production.example .env.production
docker compose --env-file .env.production -f compose.production.yaml up --build -d
docker compose --env-file .env.production -f compose.production.yaml down
```
